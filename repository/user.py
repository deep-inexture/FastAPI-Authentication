import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import tokens
from hashing import Hash


def forgot_password(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Email-ID do not Exists")
    forgot_password_token = tokens.create_forgot_password_token(data={"sub": user.email})
    return {"Reset Password Link": forgot_password_token}


def reset_password(reset_token, request, db: Session):
    email = tokens.verify_forgot_password_token(reset_token)
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect/Expired Token")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=f"Password Do not Match")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail="Password must be 8 characters long\n"
                                                    "Password must contain at-least 1 uppercase, 1 lowercase, "
                                                    "and 1 special character")

    user_data = db.query(models.User).filter(models.User.email == email).first()
    user_data.password = Hash.bcrypt(request.password)

    db.commit()
    return {"message": "Password Reset Successfully"}

