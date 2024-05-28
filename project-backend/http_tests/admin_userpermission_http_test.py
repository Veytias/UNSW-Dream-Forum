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
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token' : payload0['token'],
        'u_id' : payload1['auth_user_id'],
        'permission_id' : 1
    })

    u_permission = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token' : payload0['token'],
        'u_id' : 100,
        'permission_id' : 1
    })

    assert u_permission.status_code == 400

def test_permision_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    u_permission = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token' : payload0['token'],
        'u_id' : payload1['auth_user_id'],
        'permission_id' : 3
    })

    assert u_permission.status_code == 400

def test_auth_no_permisiion():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    u_permission = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token' : payload1['token'],
        'u_id' : payload0['auth_user_id'],
        'permission_id' : 2
    })

    assert u_permission.status_code == 403

def test_userpermission_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    u_permission = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json={
        'token' : payload0['token'],
        'u_id' : payload1['auth_user_id'],
        'permission_id' : 1
    })

    assert u_permission.status_code == 200