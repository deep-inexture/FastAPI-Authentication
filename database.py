from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Settings
import cloudinary


cloudinary.config(
    cloud_name=Settings().CLOUDINARY_CLOUD_NAME,
    api_key=Settings().CLOUDINARY_API_KEY,
    api_secret=Settings().CLOUDINARY_API_SECRET
)

engine = create_engine(Settings().DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
