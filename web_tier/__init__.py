import json
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import time
from aws_utils import upload_files_to_s3, push_to_sqs

# Change URLs and Bucket Name
queue_url = "https://sqs.us-east-1.amazonaws.com/122494296658/app-tier-first"
bucket_url = "http://s3.amazonaws.com/data-tier-input-bucket/"
bucket_name = "data-tier-input-bucket"

app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_files():
    for uploaded_file in request.files.getlist('myfile'):
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                object_name = str(time.time()) + "$" + filename
                upload_files_to_s3(uploaded_file, bucket_name, object_name)
                response = push_to_sqs(filename, object_name, queue_url)

                print(response['MessageId'])

    # Dummy response
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


app.run(
    host=os.getenv('LISTEN', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
