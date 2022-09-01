from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database import get_db
from fastAPI_authentication.authentications import oauth2, schemas, services

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)


@router.post('/register', response_model=schemas.ShowUser)
def register(request: schemas.RegisterUser, db: Session = Depends(get_db)):
    service_obj = services.Authentication(request)
    return service_obj.register(db)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service_obj = services.Authentication(request)
    return service_obj.login(db)


@router.get('/refresh_token')
def refresh_token(current_user: schemas.User = Depends(oauth2.get_current_user_refresh_token)):
    token = services.refresh_token(current_user.email)
    return {"access_token": token}


@router.post('/forgot_password')
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    service_obj = services.Authentication(request)
    return service_obj.forgot_password(db)


@router.post('/reset_password/{reset_token}')
def reset_password(reset_token: str, request: schemas.ResetPassword, db: Session = Depends(get_db)):
    service_obj = services.Authentication(request)
    return service_obj.reset_password(reset_token, db)
