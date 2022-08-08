import os
import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastAPI_authentication import models
from fastAPI_authentication.authentications import tokens
from hashing import Hash
from dotenv import load_dotenv

load_dotenv()

RESET_WEBSITE_LINK = os.environ.get('RESET_WEBSITE_LINK')


def check_password_validations(password, confirm_password):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail=f"Password Do not Match")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', password):
        raise HTTPException(status_code=400, detail="Password must be 8 characters long\n"
                                                    "Password must contain at-least 1 uppercase, 1 lowercase, "
                                                    "and 1 special character")
    return True


def register(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=f"Email-ID Already Exists")
    if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=f"Invalid Email-ID format")

    check_password_validations(request.password, request.confirm_password)

    new_user = models.User(username=request.username, email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()

    new_profile = models.UserProfile(user_id=new_user.id, profile_photo=os.environ.get('CLOUDINARY_DEFAULT'))
    db.add(new_profile)
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

    access_token = tokens.create_access_token(data={"sub": user.email})
    refreshToken = tokens.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refreshToken, "token_type": "bearer"}


def refresh_token(email):
    return tokens.create_access_token(data={"sub": email})


def forgot_password(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Email-ID do not Exists")
    forgot_password_token = tokens.create_forgot_password_token(data={"sub": user.email})
    return {"Reset Password Link": RESET_WEBSITE_LINK+'/'+forgot_password_token}


def reset_password(reset_token, request, db: Session):
    print(request.password)
    print(db.query(models.User).filter(models.User.email == 'deep@deep.in').first())
    email = tokens.verify_forgot_password_token(reset_token, HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid/Expired Token"))
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect/Expired Token")

    check_password_validations(request.password, request.confirm_password)

    email = getattr(email, 'email')

    user_data = db.query(models.User).filter(models.User.email == email).first()
    user_data.password = Hash.bcrypt(request.password)

    db.commit()
    return {"message": "Password Reset Successfully"}
