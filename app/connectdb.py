from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://yashram:yashram@localhost:5432/practice'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    '''
    This method maintains the db session per user session
    '''
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
