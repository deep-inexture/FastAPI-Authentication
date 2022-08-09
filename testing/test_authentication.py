import json
from config import Settings


def test_registration_success_200(client):
    data = {
        "username": 'TestUser2',
        "email": 'testuser2@user2.in',
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    response = client.post('authentication/register', json.dumps(data))
    assert response.status_code == 200
    assert response.json()["username"] == 'TestUser2'
    assert response.json()["email"] == 'testuser2@user2.in'


def test_registration_email_exists(client):
    data = {
        "username": 'TestUser2',
        "email": 'testuser2@user2.in',
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    response = client.post('authentication/register', json.dumps(data))
    assert response.status_code == 409
    assert response.json()['detail'] == "Email-ID Already Exists"


def test_registration_email_format(client):
    data = {
        "username": 'TestUser2',
        "email": 'TestUser2',
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    response = client.post('authentication/register', json.dumps(data))
    assert response.status_code == 401
    assert response.json()['detail'] == "Invalid Email-ID format"


def test_registration_invalid_password(client):
    data = {
        "username": 'TestUser3',
        "email": 'testuser3@user3.in',
        "password": 'testuser@1234',
        "confirm_password": 'testuser@1234'
    }
    response = client.post('authentication/register', json.dumps(data))
    assert response.status_code == 400
    assert response.json()['detail'] == "Password must be 8 characters long\nPassword must contain at-least 1 uppercase, 1 lowercase, and 1 special character"


def test_registration_password_mismatch(client):
    data = {
        "username": 'TestUser3',
        "email": 'testuser3@user3.in',
        "password": 'TestUser@1234',
        "confirm_password": 'testuser@1234'
    }
    response = client.post('authentication/register', json.dumps(data))
    assert response.status_code == 400
    assert response.json()['detail'] == "Password Do not Match"


def test_login_success_200(client, token_header):
    data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@1234"
    }

    response = client.post('authentication/login', data)
    assert response.status_code == 200
    assert response.json()['access_token'] == token_header['access']
    assert response.json()['refresh_token'] == token_header['refresh']


def test_login_invalid_credentials(client):
    data = {
        "username": "testuser10@user10.in",
        "password": "TestUser@1234"
    }

    response = client.post('authentication/login', data)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Invalid Credentials'


def test_login_invalid_password(client):
    data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@4321"
    }

    response = client.post('authentication/login', data)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Incorrect Password'


def test_forgot_password_200(client, forgot_password_token):
    data = {
        "email": "testuser1@user1.in",
    }
    response = client.post('authentication/forgot_password', json.dumps(data))
    assert  response.status_code == 200
    assert response.json()["Reset Password Link"] == Settings().RESET_WEBSITE_LINK+'/'+forgot_password_token['token']


def test_forgot_password_invalid_email(client):
    data = {
        "email": "testuser10@user10.in",
    }
    response = client.post('authentication/forgot_password', json.dumps(data))
    assert  response.status_code == 404
    assert response.json()["detail"] == "Email-ID do not Exists"


def test_reset_password_200(client, forgot_password_token):
    data = {
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    token = forgot_password_token['token']
    response = client.post('authentication/reset_password/'+token, json.dumps(data))
    assert response.status_code == 200
    assert response.json()["message"] == "Password Reset Successfully"


def test_reset_password_invalid_token(client):
    data = {
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    response = client.post('authentication/reset_password/12345', json.dumps(data))
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid/Expired Token"


def test_reset_password_password_mismatch(client, forgot_password_token):
    data = {
        "password": 'TestUser@1234',
        "confirm_password": 'testuser@1234'
    }
    token = forgot_password_token['token']
    response = client.post('authentication/reset_password/'+token, json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Password Do not Match"


def test_reset_password_invalid_password_format(client, forgot_password_token):
    data = {
        "password": 'test@1234',
        "confirm_password": 'test@1234'
    }
    token = forgot_password_token['token']
    response = client.post('authentication/reset_password/'+token, json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be 8 characters long\nPassword must contain at-least 1 uppercase, 1 lowercase, and 1 special character"


def test_refresh_token_200(client, token_header):
    response = client.get('authentication/refresh_token', headers={"Authorization": token_header['header']})
    assert response.status_code == 200
    assert response.json()["access_token"]


