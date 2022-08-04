from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import oauth2
import schemas
from oauth2 import get_current_user
from database import get_db
from repository import authentication

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)


@router.post('/register', response_model=schemas.ShowUser)
def register(request: schemas.RegisterUser, db: Session = Depends(get_db)):
    return authentication.register(request, db)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authentication.login(request, db)


@router.get('/refresh_token')
def refresh_token(current_user: schemas.User = Depends(oauth2.get_current_user_refresh_token)):
    token = authentication.refresh_token(current_user.email)
    return {"refresh_token": token}


@router.get('/user_detail')
def user_detail(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return authentication.user_detail(db)
