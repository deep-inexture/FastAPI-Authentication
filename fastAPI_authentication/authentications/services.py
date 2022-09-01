import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastAPI_authentication import models
from fastAPI_authentication.authentications import tokens
from hashing import Hash
from config import Settings


RESET_WEBSITE_LINK = Settings().RESET_WEBSITE_LINK


class Authentication:
    def __init__(self, request, ):
        self.request = request

    def check_password_validations(self, password, confirm_password):
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Password Do not Match")
        if not re.fullmatch('^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', password):
            raise HTTPException(status_code=400, detail="Password must be 8 characters long\nPassword must contain at-least 1 uppercase, 1 lowercase, and 1 special character")
        return True

    def register(self, db: Session):
        if user := db.query(models.User).filter(models.User.email == self.request.email).first():
            raise HTTPException(status_code=409, detail="Email-ID Already Exists")
        if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", self.request.email):
            raise HTTPException(status_code=401, detail="Invalid Email-ID format")

        self.check_password_validations(self.request.password, self.request.confirm_password)

        new_user = models.User(username=self.request.username, email=self.request.email,
                               password=Hash.bcrypt(self.request.password))
        db.add(new_user)
        db.commit()

        new_profile = models.UserProfile(user_id=new_user.id, profile_photo=Settings().CLOUDINARY_DEFAULT)
        db.add(new_profile)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login(self, db: Session):
        user = db.query(models.User).filter(models.User.email == self.request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Invalid Credentials")
        if not Hash.verify(user.password, self.request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Password")

        access_token = tokens.create_access_token(data={"sub": user.email})
        refreshToken = tokens.create_refresh_token(data={"sub": user.email})
        return {"access_token": access_token, "refresh_token": refreshToken, "token_type": "bearer"}

    def forgot_password(self, db: Session):
        user = db.query(models.User).filter(models.User.email == self.request.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email-ID do not Exists")
        forgot_password_token = tokens.create_forgot_password_token(data={"sub": user.email})
        return {"Reset Password Link": f'{RESET_WEBSITE_LINK}/{forgot_password_token}', "forgot_password_token": forgot_password_token}

    def reset_password(self, reset_token, db: Session):
        email = tokens.verify_forgot_password_token(reset_token, HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                               detail="Invalid/Expired Token"))
        if not email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect/Expired Token")

        self.check_password_validations(self.request.password, self.request.confirm_password)

        email = getattr(email, 'email')
        user_data = db.query(models.User).filter(models.User.email == email).first()
        user_data.password = Hash.bcrypt(self.request.password)

        db.commit()
        return {"message": "Password Reset Successfully"}


def refresh_token(email):
    return tokens.create_access_token(data={"sub": email})
