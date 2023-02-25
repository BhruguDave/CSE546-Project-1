import boto3
import json
import time

sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3')


def upload_files_to_s3(filestream, bucket_name, object_name):
    s3.upload_fileobj(filestream, bucket_name, object_name)


def push_to_sqs(file_name, s3_entry_name, queue_url):
    body = {
        'FileName': file_name,
        'S3Entry': s3_entry_name
    }
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageBody=(
            json.dumps(body)
        )
    )
    return response


def poll_from_sqs(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=1
    )
    if 'Messages' in response:
        return response['Messages']
    return []


def get_messages_from_response_queue(response_queue_url, num_of_incoming_reqs):
    responses = []
    num_of_outgoing_reqs = 0
    while num_of_outgoing_reqs != num_of_incoming_reqs:
        messages = poll_from_sqs(response_queue_url)
        num_of_outgoing_reqs += len(messages)
        for message in messages:
            receipt_handle = message['ReceiptHandle']
            response_body = json.loads(message['Body'])
            response = {
                "FileName": response_body['name'] + ".JPEG",
                "Prediction": response_body['prediction'],
            }
            responses.append(response)

            sqs.delete_message(
                QueueUrl=response_queue_url,
                ReceiptHandle=receipt_handle
            )
        time.sleep(1)

    return responses
