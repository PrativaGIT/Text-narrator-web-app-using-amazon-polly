import os
import boto3
from flask import Flask, render_template, request, send_file, flash, redirect
from werkzeug.utils import secure_filename
import io
import json
import base64

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.urandom(24)

# AWS Config
s3_client = boto3.client('s3', region_name='us-east-1')  # Set region appropriately
bucket_name = 'polly-sourcebucket'  # Replace with your S3 bucket name
lambda_client = boto3.client('lambda', region_name='us-east-1')  # Set region appropriately
lambda_name = 'TextToSpeechFunction'  # Replace with your Lambda function name

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect('/')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect('/')
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            
            # Upload the file to S3
            s3_client.upload_fileobj(file, bucket_name, filename)
            
            # Trigger Lambda function
            response = lambda_client.invoke(
                FunctionName=lambda_name,
                InvocationType='RequestResponse',
                Payload=json.dumps({'bucket': bucket_name, 'filename': filename})
            )
            
            # Get the response from Lambda
            response_payload = json.loads(response['Payload'].read().decode())
            
            if response_payload.get('statusCode') == 200:
                # Decode the base64-encoded audio
                audio_content_base64 = response_payload['body']
                audio_content = base64.b64decode(audio_content_base64)
                
                # Return the audio file to the user for download
                return send_file(io.BytesIO(audio_content),
                                 mimetype='audio/mpeg',
                                 as_attachment=True,
                                 download_name=filename.replace('.txt', '.mp3'))
            else:
                flash(f"Error: {response_payload.get('body')}", 'error')
                return redirect('/')
        
        except Exception as e:
            flash(f'Error processing the file: {str(e)}', 'error')
            return redirect('/')
    
    flash('Invalid file type. Please upload a .txt file.', 'error')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
