from datetime import timedelta, datetime
from jose import JWTError, jwt
from . import schemas
from config import Settings


FORGOT_PASSWORD_SECRET_KEY = Settings().FORGOT_PASSWORD_SECRET_KEY
SECRET_KEY = Settings().SECRET_KEY
JWT_REFRESH_SECRET_KEY = Settings().JWT_REFRESH_SECRET_KEY
ALGORITHM = Settings().ALGORITHM
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
        if email := payload.get("sub"):
            token_data = schemas.TokenData(email=email)
        else:
            raise credentials_exception
        return token_data
    except JWTError as e:
        raise credentials_exception from e


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if email := payload.get("sub"):
            token_data = schemas.TokenData(email=email)
        else:
            raise credentials_exception
        return token_data
    except JWTError as e:
        raise credentials_exception from e


def create_forgot_password_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=FORGOT_PASSWORD_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, FORGOT_PASSWORD_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_forgot_password_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, FORGOT_PASSWORD_SECRET_KEY, algorithms=[ALGORITHM])
        if email := payload.get("sub"):
            token_data = schemas.TokenData(email=email)
        else:
            raise credentials_exception
        return token_data
    except JWTError as e:
        raise credentials_exception from e
