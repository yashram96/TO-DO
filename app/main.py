from fastapi import FastAPI,Request

from fastapi_paseto_auth import AuthPASETO
from fastapi_paseto_auth.exceptions import AuthPASETOException
from fastapi.responses import JSONResponse
from . import models, request_schemas as schema
from .routes import auth,users
from app.connectdb import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@AuthPASETO.load_config
def get_config():
    return schema.PasetoKey()

@app.exception_handler(AuthPASETOException)
def authpaseto_exception_handler(request: Request, exc: AuthPASETOException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}