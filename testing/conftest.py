import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def token_header(client: TestClient):
    data = {
        "username": 'TestUser1',
        "email": 'testuser1@user1.in',
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    client.post('authentication/register', json.dumps(data))
    login_data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@1234"
    }
    response = client.post("authentication/login", data=login_data)
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    return {'header': f"Bearer {access_token}", 'access': access_token, 'refresh': refresh_token}


@pytest.fixture
def forgot_password_token(client: TestClient):
    data = {
        "email": "testuser1@user1.in"
    }
    response = client.post("authentication/forgot_password", json.dumps(data))
    token = response.json()['Reset Password Link'].split('/')[-1]
    return {'token': token}