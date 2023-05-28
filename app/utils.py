from passlib.context import CryptContext
from app.models.common import TimeZones
import pytz
from sqlalchemy.orm import Session
from fastapi import status,HTTPException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def fill_timezone(db : Session, timezone : str):

    if db.query(TimeZones).count() == 0:
        try:
            zones = pytz.all_timezones
            values = [{"timezone_name": value} for value in zones]
            db.add_all(TimeZones(**value) for value in values)
            db.commit() 
        except Exception as err:
            db.rollback()
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= {'status' : 'Success' , 'data' : [{}] , 'message': f'{err} in fill_timezone' })
    timezone_id = db.query(TimeZones).filter(TimeZones.timezone_name == timezone).with_entities(TimeZones.id).scalar()
    print(f'timezone_id_new is {timezone_id}')
    return timezone_id

    

