from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
import os
from aws_utils import upload_files_to_s3, push_to_sqs, poll_from_sqs, get_messages_from_response_queue

# Change URLs and Bucket Name
request_queue_url = "https://sqs.us-east-1.amazonaws.com/125035222225/ec3_request_queue"
response_queue_url = "https://sqs.us-east-1.amazonaws.com/125035222225/ec3_response_queue"
bucket_url = "http://s3.amazonaws.com/cse-546-ec3-input-bucket/"
bucket_name = "cse-546-ec3-input-bucket"

app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_files():
    num_of_incoming_reqs = 0
    for uploaded_file in request.files.getlist('myfile'):
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                num_of_incoming_reqs += 1
                object_name = filename
                upload_files_to_s3(uploaded_file, bucket_name, object_name)
                confirmation = push_to_sqs(filename, object_name, request_queue_url)
                print("Published to Request SQS Queue with MessageId: ", confirmation['MessageId'])

    responses = get_messages_from_response_queue(response_queue_url, num_of_incoming_reqs)
    for response in responses:
        return make_response(jsonify(response), 200)


app.run(
    host=os.getenv('LISTEN', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
