from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from fastAPI_authentication.users import schemas, services
from database import get_db
from fastAPI_authentication.authentications.oauth2 import get_current_user

import cloudinary
import cloudinary.uploader

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.put('/update_profile')
def update_profile(request: schemas.Profile = Depends(), file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):
    print('-----------------------------')
    print(file)
    print('-----------------------------')
    profile_photo = cloudinary.uploader.upload(file.file)
    url = profile_photo.get("url")
    service_obj = services.UserProfile(request)
    return service_obj.update_profile(url, current_user.email)


@router.get('/show_user_profile', response_model=schemas.BaseProfile)
def user_profile(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return services.user_profile(db, current_user.email)


@router.put('/change_password')
def change_my_password(request: schemas.ChangePassword, current_user: schemas.User = Depends(get_current_user)):
    service_obj = services.UserProfile(request)
    return service_obj.change_my_password(current_user.email)
