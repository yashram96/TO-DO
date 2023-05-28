from fastapi import  status, HTTPException, Depends, APIRouter

from app.models.user import Users,UserPreferences
from app.models.common import TimeZones
from .. import request_schemas as schema, utils
from app.connectdb import  get_db
from sqlalchemy.orm import Session ,attributes
from fastapi_paseto_auth import AuthPASETO
from sqlalchemy import Join

REFERER_SCRECT = 'DEMO_PROJECT'

router = APIRouter(
    tags=["Users"],
    prefix ="/v1/users"
)   

@router.post("/signup", status_code=status.HTTP_201_CREATED , response_model= schema.UserSuccess)
async def create_user(user : schema.CreateUser ,db: Session = Depends(get_db) ):

    if user.referer_secret != REFERER_SCRECT :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message': f'You are not authorized to signup' })
    
    response_columns = list(schema.User.__fields__.keys())

    hashed_password = utils.hash(user.password)
    user.password = hashed_password 
    user_refined = user.dict()  
    user_refined = {x: user_refined[x] for x in user_refined if x not in ['referer_secret','timezone_name','reactivate']}
    new_user  = Users(**user_refined)
    new_timezone_id = utils.fill_timezone(db,str(user.timezone_name))
    
    if new_timezone_id is not None:
        try:
            if not user.reactivate:
                db.add(new_user)
                db.flush() # Synchronize the session with the database, but don't commit the transaction yet
                print(f'new user id = {new_user.id}') # Access the ID of the new user record
                user_preferences = UserPreferences(user_id = new_user.id , timezone_id = new_timezone_id)
                db.add(user_preferences)
                db.commit()  
                db.refresh(new_user)
                new_user = db.query(Users,TimeZones).join(UserPreferences, Users.id == UserPreferences.user_id).join(TimeZones , UserPreferences.timezone_id == TimeZones.id).filter(Users.username == new_user.username).first()

            else :
                new_user = db.query(Users,TimeZones).join(UserPreferences, Users.id == UserPreferences.user_id).join(TimeZones , UserPreferences.timezone_id == TimeZones.id).filter(Users.username == new_user.username).first()
                new_user[0].is_active = True
                db.commit()  
            userresponse = schema.User(
                **{column: getattr(new_user[0], column) if column in dir(new_user[0]) else getattr(new_user[1], column) for column in response_columns}
            )

            return {'status' : 'Success' , 'data' : [userresponse] }
        except Exception as err:
            db.rollback()
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message': f'{err}' })
    else :
        db.rollback()
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Failed' , 'data' : [{}] , 'message': f'Timezone{user.timezone} is not valid '})
    

@router.get('/delete/{username}' ,status_code=status.HTTP_202_ACCEPTED, response_model= schema.UserSuccess)
async def del_account(username : str , db: Session = Depends(get_db),Authorize: AuthPASETO = Depends() ):
    Authorize.paseto_required()
    user_info = db.query(Users,TimeZones).join(UserPreferences, Users.id == UserPreferences.user_id).join(TimeZones , UserPreferences.timezone_id == TimeZones.id).filter(Users.username == username,Users.is_active == True).first()

    if Authorize._current_user == username:
        try:
            user_info[0].is_active = False
            db.commit()  
            message = 'Delete success'
        except Exception as err:
            db.rollback()
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message': f'{err}' })
    else :
        raise HTTPException(status_code= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION , detail= {'status' : 'Success' , 'data' : [{}] , 'message':f'You are not authorised to delete other account' })

    response_columns = list(schema.User.__fields__.keys())
    userresponse = schema.User(
        **{column: getattr(user_info[0], column) if column in dir(user_info[0]) else getattr(user_info[1], column) for column in response_columns}
    )
    
    return {'status' : 'Success' , 'data' : [userresponse] , 'message' : message}


@router.get('/{username}', response_model= schema.UserSuccess)
async def get_user(username : str , db: Session = Depends(get_db),Authorize: AuthPASETO = Depends() ):
    Authorize.paseto_required()
    user_info = db.query(Users,TimeZones).join(UserPreferences, Users.id == UserPreferences.user_id).join(TimeZones , UserPreferences.timezone_id == TimeZones.id).filter(Users.username == username and Users.is_active == True).first()
    if not user_info: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message':f'{username} is not a valid username' })
    elif Authorize._current_user != username:
        raise HTTPException(status_code= status.HTTP_203_NON_AUTHORITATIVE_INFORMATION , detail= {'status' : 'Success' , 'data' : [{}] , 'message':f'You cant check user details unless {username} is in your friends list' })

    response_columns = list(schema.User.__fields__.keys())

    userresponse = schema.User(
        **{column: getattr(user_info[0], column) if column in dir(user_info[0]) else getattr(user_info[1], column) for column in response_columns}
    )
    return {'status' : 'Success' , 'data' : [userresponse] }