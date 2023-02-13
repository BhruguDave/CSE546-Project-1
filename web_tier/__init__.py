from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_files():
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                print("Will upload file from here")

                # Get the queue. This returns an SQS.Queue instance

    # Dummy response
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


app.run(
    host=os.getenv('LISTEN', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080'))
)
