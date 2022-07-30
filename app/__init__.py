from fastapi import FastAPI
from app.handlers.auth import use_auth
from app.handlers.upload import app as upload_app

def app():
    _ = use_auth(FastAPI())
    _.include_router(upload_app, prefix='/api', tags=['upload'])
    @_.get("/")
    def root():
        return {"message": "Hello World"}
    return _
