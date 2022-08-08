from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from .. import schemas
from database import get_db
from fastAPI_authentication.authentications.oauth2 import get_current_user
from fastAPI_authentication.users.repository import user

import cloudinary
import cloudinary.uploader

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.put('/update_profile')
def update_profile(request: schemas.Profile = Depends(), file: UploadFile = File(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    profile_photo = cloudinary.uploader.upload(file.file)
    url = profile_photo.get("url")
    return user.update_profile(request, url, db, current_user.email)


@router.get('/show_user_profile', response_model=schemas.BaseProfile)
def user_profile(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.user_profile(db, current_user.email)


@router.put('/change_password')
def change_my_password(request: schemas.ChangePassword, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.change_my_password(request, db, current_user.email)
