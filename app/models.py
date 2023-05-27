from .connectdb import Base,engine
from sqlalchemy import Column , Integer,String ,MetaData
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, NUMERIC



class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'to_do'}

    id = Column(Integer, primary_key = True, nullable = False ) 
    username = Column(String , unique =True) 
    firstname = Column(String) 
    password = Column(String, nullable = False ) 
    email = Column(String , nullable = False , unique =True)
    role = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))
    updated_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))
