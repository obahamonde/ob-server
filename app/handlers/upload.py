from fastapi import UploadFile, File, Request, APIRouter
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from typing import List, Dict, Union, Optional
from pydantic import HttpUrl
from app.models.schemas import User, Upload
from app.handlers.auth import user_info
from app.config import environ


AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = environ.get('AWS_REGION_NAME')
AWS_S3_BUCKET = environ.get('AWS_S3_BUCKET')

s3 = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
).client('s3')

def upload_file(file: UploadFile)->HttpUrl:
    try:
        s3.upload_fileobj(
            file.file,
            AWS_S3_BUCKET,
            file.filename,
            ExtraArgs={
                'ContentType': file.content_type,
                'ACL': 'public-read'
            }
        )
        
    except (BotoCoreError, ClientError) as e:
        raise e
    return f'https://{AWS_S3_BUCKET}.s3.amazonaws.com/{file.filename}'

app = APIRouter()

@app.post('/upload')
async def upload_file_to_s3(request: Request, file: UploadFile = File(...)):
    return Upload(
        sub=request.state.user['sub'],
        filename=file.filename,
        mimetype=file.content_type,
        url=upload_file(file)
    ).create()