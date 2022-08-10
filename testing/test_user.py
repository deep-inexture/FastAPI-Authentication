import json


def test_update_profile_200(client, token_header):
    file = '/home/deep/Pictures/default.png'
    data = {
        "name": 'TestUser',
        "phone": '1234567890',
        "gender": 'Male',
        # "file" : open(file, 'rb')
    }
    files = {"file": ("file", open(file, "rb"), "image/jpeg")}
    response = client.put('/user/update_profile', data=data, files=files, headers={"Authorization": token_header['header']})
    print(response)
    print(response.json())
    # assert response.status_code == 200
    # assert response.json()['message'] == 'Profile Updated Successfully'


def test_user_profile_200(client, token_header):
    response = client.get('/user/show_user_profile', headers={"Authorization": token_header['header']})
    assert response.status_code == 200
    assert response.json()['owner']['username'] == 'TestUser1'
    assert response.json()['owner']['email'] == 'testuser1@user1.in'


# def test_change_password_200(client, token_header):
#     data = {
#         'new_password': 'TestUser@1234',
#         'confirm_new_password': 'TestUser@1234'
#     }
#     response = client.put('/user/change_password', json.dumps(data), headers={"Authorization": token_header['header']})
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Password Changed Successfully'
