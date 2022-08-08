import re

from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastAPI_authentication import models
from hashing import Hash


def check_password_validations(password, confirm_password):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail=f"Password Do not Match")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', password):
        raise HTTPException(status_code=400, detail="Password must be 8 characters long\n"
                                                    "Password must contain at-least 1 uppercase, 1 lowercase, "
                                                    "and 1 special character")
    return True


def update_profile(request, url, db: Session, email):
    profile_setting = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == db.query(models.User.id).filter(
            models.User.email == email)).first()
    profile_setting.profile_photo = url
    profile_setting.name = request.name
    profile_setting.phone = request.phone
    profile_setting.gender = request.gender

    db.commit()
    return {'message': 'Profile Updated Successfully'}


def user_profile(db: Session, email):
    return db.query(models.UserProfile).filter(
        models.UserProfile.user_id == db.query(models.User.id).filter(
            models.User.email == email)).first()


def change_my_password(request, db, email):
    fetch_user = db.query(models.User).filter(models.User.email == email).first()

    check_password_validations(request.new_password, request.confirm_new_password)

    fetch_user.password = Hash.bcrypt(request.new_password)
    db.commit()

    return {"message": "Password Changed Successfully"}
