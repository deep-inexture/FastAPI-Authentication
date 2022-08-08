from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_token(token, credentials_exception)


def get_current_user_refresh_token(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate ACCESS TOKEN",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_refresh_token(data, credentials_exception)