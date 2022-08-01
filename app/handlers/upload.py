from fastapi import UploadFile, File, Request, APIRouter
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from pydantic import HttpUrl
from app.models.schemas import Upload
from app.config import environ
from app.utils import uuid4
from urllib.parse import quote

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = environ.get('AWS_REGION_NAME')
AWS_S3_BUCKET = environ.get('AWS_S3_BUCKET')

s3 = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
).client('s3')

def upload_file(key:str,file: UploadFile)->HttpUrl:
    try:
        s3.upload_fileobj(
            file.file,
            AWS_S3_BUCKET,
            key,
            ExtraArgs={
                'ContentType': file.content_type,
                'ACL': 'public-read'
            }
        )
        
    except (BotoCoreError, ClientError) as e:
        raise e
    return f'https://{AWS_S3_BUCKET}.s3.amazonaws.com/{file.filename}'

app = APIRouter()

@app.post('/upload/{size}')
async def upload_file_to_s3(request: Request, size:float, file: UploadFile = File(...)):
    sub=request.state.user.sub
    fid=uuid4().hex
    url = upload_file(f'{sub}/{fid}/{file.filename}', file)
    return Upload(
        
        sub=sub,
        filename=file.filename,
        url=url,
        mimetype=file.content_type,
        size=size
    ).create()

@app.get('/upload')
async def get_uploads(request:Request):
    sub = request.state.user.sub
    return Upload.find_many("sub",sub,10)

