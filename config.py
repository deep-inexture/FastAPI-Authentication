from pydantic import BaseSettings


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
        env_file = '.env'
