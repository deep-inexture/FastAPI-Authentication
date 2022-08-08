import os
import re

from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastAPI_authentication import models
from hashing import Hash


class UserProfile:
    def __init__(self, request):
        self.request = request

    def check_password_validations(self, password, confirm_password):
        if password != confirm_password:
            raise HTTPException(status_code=400, detail=f"Password Do not Match")
        if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', password):
            raise HTTPException(status_code=400, detail="Password must be 8 characters long\n"
                                                        "Password must contain at-least 1 uppercase, 1 lowercase, "
                                                        "and 1 special character")
        return True

    def update_profile(self, url, email):
        models.UserProfile.update_profile(self.request.name, self.request.phone,
                                          self.request.gender, url, email)
        return {'message': 'Profile Updated Successfully'}

    def change_my_password(self, email):
        if self.check_password_validations(self.request.new_password, self.request.confirm_new_password):
            models.User.change_password(email, self.request.new_password)

        return {"message": "Password Changed Successfully"}


def user_profile(db: Session, email):
    return db.query(models.UserProfile).filter(
        models.UserProfile.user_id == db.query(models.User.id).filter(
            models.User.email == email)).first()
