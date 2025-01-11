import os
import boto3
from flask import Flask, render_template, request, send_file, flash, redirect
from werkzeug.utils import secure_filename
import io
import json
import base64

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for session management (should be kept secret)
app.secret_key = os.urandom(24)  # Or set a custom key if needed

# AWS Config
s3_client = boto3.client('s3', region_name='ap-south-1')
bucket_name = 'polly-sourcebucket'  
lambda_client = boto3.client('lambda', region_name='ap-south-1') 
lambda_name = 'TextToSpeechFunction'
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
        print("No file part")
        return redirect('/')
    
    file = request.files['file']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        flash('No selected file', 'error')
        print("No selected file")
        return redirect('/')
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_content = file.read().decode('utf-8')  # Read content as a string

            # Reset the file pointer to the beginning
            file.seek(0)
            
            # Upload the file to S3
            s3_client.upload_fileobj(file, bucket_name, filename)
            print(f"File uploaded to S3: {filename} with content: {file_content} ")
            
            # Trigger Lambda function
            response = lambda_client.invoke(
                FunctionName=lambda_name,  # Replace with your Lambda function name
                InvocationType='RequestResponse',
                Payload=json.dumps({'bucket': bucket_name, 'filename': filename})
            )
            print('response: ',response)
            
            # Get the audio content from Lambda response
            response_payload = json.loads(response['Payload'].read())
            print(f"Lambda response: {response_payload}")
            
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
                print(f"Error: {response_payload.get('body')}")
                return redirect('/')
        
        except Exception as e:
            flash(f'Error processing the file: {str(e)}', 'error')
            print(f'Error processing the file: {str(e)}')
            return redirect('/')
    
    flash('Invalid file type. Please upload a .txt file.', 'error')
    print('Invalid file type. Please upload a .txt file.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
