import boto3
import json


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
