from app.config import environ
from app.lib import net
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
from app.models.schemas import User

AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
AUTH0_API_AUDIENCE = environ.get('AUTH0_API_AUDIENCE')
AUTH0_API_SCOPE = environ.get('AUTH0_API_SCOPE')
AUTH0_API_GRANT_TYPE = environ.get('AUTH0_API_GRANT_TYPE')


async def user_info(token: str):
    url = f'https://{environ.get("AUTH0_DOMAIN")}/userinfo'
    headers = {'Authorization': f'Bearer {token}'}
    response = await net._fetch(url, headers)
    return response



def user(request:Request):
    return request.state.user

def use_auth(app:FastAPI)->FastAPI:
    @app.middleware('http')
    async def auth_client(request:Request, call_next:Callable):
        if request.url.path.find('/api/') == 0:
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                u = await user_info(token)
                user = User(**u).save()
                request.state.user = user
            except Exception as e:
                raise e
        return await call_next(request)
    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
    return app