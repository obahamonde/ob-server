from pydantic import HttpUrl, EmailStr, Field
from typing import Optional, Union, Any, List, Dict
from app.lib.fql import FQLModel as Q
from app.utils import get_avatar, uid



class User(Q):
    sub: str = Field(...)
    given_name: Optional[str] = Field()
    family_name: Optional[str] = Field()
    nickname: Optional[str] = Field()
    name: Optional[str] = Field()
    picture: Optional[Union[HttpUrl, str]] = Field(default_factory=get_avatar)
    locale: Optional[Union[str, None]] = Field()
    updated_at: Optional[str] = Field()
    email: Union[EmailStr, str, None] = Field(index=True)
    email_verified: Optional[Union[bool, str]] = Field()

class Upload(Q):
    id: str = Field(default_factory=uid, index=True)
    sub: str = Field(..., index=True)
    filename: Optional[str] = Field()
    size: Optional[float] = Field()
    mimetype: Optional[str] = Field()
    url: Optional[Union[HttpUrl, str]] = Field()

class Email (Q):
    from_:Union[EmailStr, str, Any] = Field(index=True)
    to:Union[EmailStr, str, Any] = Field(index=True)
    subject:Optional[str] = Field()
    body:Optional[str] = Field()
    
    
class Product(Q):
    sub: str = Field(..., index=True)
    title: str = Field(...)
    subtitle: Optional[str] = Field()
    description: Optional[str] = Field()
    tags:Optional[List[str]] = Field()
    price:float=Field(...)
    uploads:List[HttpUrl] = Field(default_factory=list)
    
    
class IAMPolicy(Q):
    arn:str = Field(...)
    version:str = Field(...)
    principals:List[str] = Field(default_factory=list)
    resources:List[str] = Field(default_factory=list)
    actions:List[str] = Field(default_factory=list)
    statements:List[Dict[str,Any]] = Field(default_factory=list)

