**Description:**

This project is a web-based application that allows users to upload text files through a user-friendly interface. Upon uploading, the text file is stored in an AWS S3 bucket. An AWS Lambda function is triggered automatically to process the uploaded file and convert its content into an audio file using Amazon Polly. The audio file is then made available for download directly to the user's local system.

![Text narrator web app using amazon polly](https://github.com/user-attachments/assets/a8eb6a33-cc9b-4860-8226-002c243867a6)

**Key Features:**
1. **User-Friendly Interface**:
   - A modern, responsive HTML interface with CSS styling for ease of use.
   - File upload functionality with support for `.txt` files only.

2. **Backend Workflow:**
   - File upload handling using Flask and secure file validation.
   - Uploaded files are stored in an AWS S3 bucket.

3. **AWS Integration:**
   - **Amazon S3**: Used for securely storing the uploaded text files.
   - **AWS Lambda**: Automatically triggered when a file is uploaded to the S3 bucket.
   - **Amazon Polly**: Converts the text content into natural-sounding speech in MP3 format.

4. **Downloadable Audio Files:**
   - Users can download the generated audio file directly after processing.

**Technical Stack:**
- **Frontend**:
  - HTML5, CSS for the user interface.
  - Flask framework for handling HTTP requests.

- **Backend**:
  - Flask (Python) for routing and handling file uploads.
  - Boto3 SDK for AWS service integration.

- **AWS Services:**
  - S3 Bucket: Storage of uploaded files.
  - Lambda: Backend processing and Polly invocation.
  - Polly: Text-to-speech conversion.

**Setup and Execution:**
1. **AWS Configuration:**
   - Create an S3 bucket for storing text files.
   - Deploy a Lambda function with permissions to access S3 and Polly.
   - Configure the Lambda function to trigger on S3 upload events.

2. **Flask Application Setup:**
   - Install Flask and Boto3 libraries.
   - Create routes for file upload and download functionalities.
   - Use Flask's `send_file` method to provide audio files for download.

3. **Execution:**
   - Run the Flask application locally.
   - Open the web interface, upload a text file, and download the converted audio file.

**Challenges Overcome:**
- Ensuring file integrity during the upload and processing stages.
- Managing AWS permissions for seamless interaction between services.
- Optimizing the Lambda function to handle edge cases, such as empty or invalid text files.

**Achievements:**
- Successfully integrated multiple AWS services for an end-to-end automated solution.
- Built a robust, scalable, and user-friendly application.
- Demonstrated expertise in cloud computing, Python, and web development.
