import json
from config import Settings


def test_registration_success_200(client):
    data = {
        "username": 'Deep',
        "email": 'deep@deep.in',
        "password": 'Deep@1234',
        "confirm_password": 'Deep@1234'
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 200
    assert response.json()["username"] == 'Deep'
    assert response.json()["email"] == 'deep@deep.in'
