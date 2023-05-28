from app.connectdb import Base
from sqlalchemy import Column , Integer,String 
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship



class TimeZones(Base):
    __tablename__ = "timezones"
    __table_args__ = {'schema': 'to_do'}

    id = Column(Integer, primary_key= True,nullable=False)
    timezone_name = Column(String, unique = True, nullable= False)
    created_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))
    updated_at = Column(TIMESTAMP(timezone= False),nullable =False , server_default = text('now()'))

    #userpreferences =  relationship('UserPreferences' , backref= 'users')
