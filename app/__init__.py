from fastapi import FastAPI
from app.handlers.auth import use_auth
from app.handlers.upload import app as upload_app
from app.handlers.email import app as email_app
from app.utils import log

def app():
    _ = use_auth(FastAPI())
    _.include_router(upload_app, prefix='/api', tags=['upload'])
    _.include_router(email_app, tags=['email'])
    log("See the docs at: http://localhost:8000/docs ")    
    return _

