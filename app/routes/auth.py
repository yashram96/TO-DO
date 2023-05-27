from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from fastapi_paseto_auth import AuthPASETO

from sqlalchemy.orm import Session 
from app.connectdb import engine, get_db
from .. import models , request_schemas as schema, utils, oauth2



router = APIRouter(
    tags=["Authenticaion"],
     prefix ="/v1"
)


@router.post('/login',status_code= status.HTTP_201_CREATED)
async def user_login(credentials :schema.UserLogin, Authorize: AuthPASETO = Depends() ,db: Session = Depends(get_db) ):

    user = db.query(models.Users).filter(models.Users.username == credentials.username).first()
    if not user: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message':f'Invalid username' })

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message':f'Invalid password' })


    access_token = Authorize.create_access_token(subject= user.username,expires_time= oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {'status' : 'Success' , 'data' : {'access_token' : access_token , 'token_type': 'bearer'} }

