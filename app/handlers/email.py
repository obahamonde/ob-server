from fastapi import APIRouter
from boto3 import Session
from app.config import environ
from app.models.schemas import Email
from app.lib.fql import FQLModel as Q

app = APIRouter()

ses = Session(
    aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=environ.get("AWS_REGION")
).client("ses")

@app.post("/email")
async def email(email: Email):
    email.save()
    await ses.send_email(
        Source=environ.get("AWS_SES_SOURCE"),
        Destination={
            "ToAddresses": [email.from_,email.to]
        },
        Message={
            "Subject": {
                "Data": email.subject
            },
            "Body": {
                "Text": {
                    "Data": email.body
                }
            }
            
        }
    )
    return {"message": "Email sent"}