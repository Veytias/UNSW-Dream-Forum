import requests
from src import config
BASE_URL =  config.url

def test_u_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })

    rm = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json={
        'token' : payload0['token'],
        'u_id' : 100
    })

    assert rm.status_code == 400

def test_one_dream_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })

    rm = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json={
        'token' : payload0['token'],
        'u_id' : payload0['auth_user_id']
    })

    assert rm.status_code == 400

def test_auth_no_permisiion():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 =  user2.json()

    rm = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json={
        'token' : payload1['token'],
        'u_id' : payload0['auth_user_id']
    })

    assert rm.status_code == 403

def test_remove_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 =  user2.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload1['token'],
        'name': 'Test Channel 2',
        'is_public': True
    })
    payload2 = channel.json()

    requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token': payload0['token'],
        'u_id': payload1['auth_user_id'],
        'permission_id' : 1
    })

    requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
    })

    rm = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json={
        'token' : payload0['token'],
        'u_id' : payload1['auth_user_id'],
    })

    assert rm.status_code == 200

