import os
from datetime import timedelta, datetime
from jose import JWTError, jwt
import schemas
from dotenv import load_dotenv

load_dotenv()

FORGOT_PASSWORD_SECRET_KEY = os.environ.get('FORGOT_PASSWORD_SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = "HS256"
FORGOT_PASSWORD_EXPIRE_MINUTES = 60
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)

        return token_data
    except JWTError:
        raise credentials_exception


def create_forgot_password_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=FORGOT_PASSWORD_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, FORGOT_PASSWORD_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_forgot_password_token(token: str):
    payload = jwt.decode(token, FORGOT_PASSWORD_SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    return email
