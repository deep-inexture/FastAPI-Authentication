from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=0)

    profile = relationship('UserProfile', back_populates='owner')


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    profile_photo = Column(String(255), default='default.png')
    name = Column(String(255), default='')
    phone = Column(String(20), default='')
    gender = Column(String(20), default='')

    owner = relationship('User', back_populates='profile')