from pydantic import HttpUrl, EmailStr, Field
from typing import Optional, Union
from uuid import UUID, uuid4
from app.lib.fql import FQLModel as Q
from app.utils import get_avatar

def uid():
    return uuid4().hex

class User(Q):
    sub: Union[str, UUID] = Field(default_factory=uid, index=True)
    given_name: Optional[str] = Field()
    family_name: Optional[str] = Field()
    nickname: str = Field(..., index=True)
    name: Optional[str] = Field()
    picture: Optional[Union[HttpUrl, str]] = Field(default_factory=get_avatar)
    locale: Optional[Union[str, None]] = Field()
    updated_at: Optional[str] = Field()
    email: Union[EmailStr, str, None] = Field(index=True)
    email_verified: Optional[Union[bool, str]] = Field()

class Upload(Q):
    id: Union[str, UUID] = Field(default_factory=uid, index=True)
    sub: Union[str, UUID] = Field(..., index=True)
    filename: Optional[str] = Field()
    mimetype: Optional[str] = Field()
    url: Optional[HttpUrl] = Field()
