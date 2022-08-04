import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import tokens
from hashing import Hash


def register(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=f"Email-ID Already Exists")
    if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=f"Invalid Email-ID format")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=f"Password Do not Match")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail="Password must be 8 characters long\n"
                                                    "Password must contain at-least 1 uppercase, 1 lowercase, "
                                                    "and 1 special character")

    new_user = models.User(username=request.username, email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password")

    access_token = tokens.create_access_token(data={"sub": user.username})
    refreshToken = tokens.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refreshToken, "token_type": "bearer"}


def refresh_token(email):
    return tokens.create_access_token(data={"sub": email})


def user_detail(db: Session):
    return db.query(models.User).all()
