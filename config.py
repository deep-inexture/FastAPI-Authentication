from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_URL: str

    FORGOT_PASSWORD_SECRET_KEY: str
    SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str

    RESET_WEBSITE_LINK: str

    CLOUDINARY_DEFAULT: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        # parent = Path.cwd()
        # env_file = f'{parent}/.env'  # set the env file path.
        env_file = '.env'
        # env_file_encoding = 'utf-8'
