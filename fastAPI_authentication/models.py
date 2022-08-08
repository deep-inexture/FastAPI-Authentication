from database import Base, get_db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from hashing import Hash

db = next(get_db())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=0)

    profile = relationship('UserProfile', back_populates='owner')

    @classmethod
    def change_password(cls, email, new_password):
        try:
            fetch_user = db.query(cls).filter(cls.email == email).first()
            fetch_user.password = Hash.bcrypt(new_password)
            db.commit()
        except SQLAlchemyError as e:
            print('msg :', e)
            return None


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    profile_photo = Column(String(255), default='default.png')
    name = Column(String(255), default='')
    phone = Column(String(20), default='')
    gender = Column(String(20), default='')

    owner = relationship('User', back_populates='profile')

    @classmethod
    def update_profile(cls, name, phone, gender, url, email):
        try:
            profile_setting = db.query(cls).filter(
                cls.user_id == db.query(User.id).filter(
                    User.email == email)).first()

            profile_setting.profile_photo = url
            profile_setting.name = name
            profile_setting.phone = phone
            profile_setting.gender = gender

            db.commit()
        except SQLAlchemyError as e:
            print('msg :', e)
            return None