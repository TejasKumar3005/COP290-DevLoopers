from flask import redirect, session
from functools import wraps
import boto3
import os
from werkzeug.utils import secure_filename

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    if session.get("user_id") is None:
        return 0
    return 1

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        # Open the file in binary mode before uploading to S3
        with file.stream as f:
            s3.upload_fileobj(
                f,
                os.getenv("AWS_BUCKET_NAME"),
                filename,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                }
            )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_safe(file):

    # check whether a file is selected
    if file.filename == '':
        return "no file selected"

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)
        
        # if upload success,will return file name of uploaded file
        if output:
            # write your code here 
            # to save the file name in database
            return file.filename

        # upload failed, redirect to upload page
        else:
            return "Unable to upload, try again"
        
    # if file extension not allowed
    else:
        return "File type not accepted,please try again."