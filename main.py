from fastapi import FastAPI

from fastAPI_authentication import models
from database import engine
from fastAPI_authentication.authentications.routers import authentication
from fastAPI_authentication.users.routers import user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)