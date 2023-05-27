from fastapi import  status, HTTPException, Depends, APIRouter 
from .. import models , request_schemas as schema, utils
from app.connectdb import  get_db
from sqlalchemy.orm import Session 
from fastapi_paseto_auth import AuthPASETO

REFERER_SCRECT = 'DEMO_PROJECT'

router = APIRouter(
    tags=["Users"],
    prefix ="/v1/users"
)   

@router.get('/{username}' , response_model= schema.UserSuccess)
async def get_user(username : str , db: Session = Depends(get_db),Authorize: AuthPASETO = Depends() ):
    Authorize.paseto_required()
    user_info = db.query(models.Users).filter(models.Users.username == username ).first()
    if not user_info: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message':f'{username} is not a valid username' })
    return {'status' : 'Success' , 'data' : [user_info] }



@router.post("/signup", status_code=status.HTTP_201_CREATED , response_model= schema.UserSuccess)
async def create_user(user : schema.CreateUser ,db: Session = Depends(get_db) ):

    if user.referer_secret != REFERER_SCRECT :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message': f'You are not authorized to signup' })
 

    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    user_refined = user.dict()  
    user_refined = {x: user_refined[x] for x in user_refined if x not in ['referer_secret']}
    new_user  = models.Users(**user_refined)

    try:
        db.add(new_user)
        db.commit()  
        db.refresh(new_user)
        return {'status' : 'Success' , 'data' : [new_user] }
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message': f'{err}' })
    else :
        db.rollback()
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message': 'Internal error'})