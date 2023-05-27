from pydantic import BaseModel ,EmailStr 
from typing import Optional
from . import oauth2

class User(BaseModel):
    username : str
    email : EmailStr
    role : str
    firstname : str

    class Config:
        orm_mode = True

class CreateUser(User):
    password : str
    referer_secret : str


class UserSuccess(BaseModel):
    status : str
    data : list[User]
    message : Optional[str] = 'Status 1'

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username : str    
    password : str

class PasetoKey(BaseModel):
    authpaseto_secret_key : str = oauth2.SECRET_KEY