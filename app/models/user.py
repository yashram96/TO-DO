from app.connectdb import Base
from sqlalchemy import Column , Integer,String,ForeignKey ,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'to_do'}

    id = Column(Integer, primary_key = True, nullable = False ) 
    username = Column(String , unique =True) 
    firstname = Column(String) 
    password = Column(String, nullable = False ) 
    email = Column(String , nullable = False , unique =True)
    role = Column(String , nullable = False)
    is_active = Column(Boolean , server_default= text('true') ,nullable = False)
    created_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))
    updated_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    __table_args__ = {'schema':'to_do'}

    id = Column(Integer , primary_key= True , nullable= False)
    user_id = Column(Integer , ForeignKey("to_do.users.id"), nullable= False)
    timezone_id = Column(Integer, ForeignKey("to_do.timezones.id"),nullable= False)
    created_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))
    updated_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))


