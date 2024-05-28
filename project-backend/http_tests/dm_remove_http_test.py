import requests
from src import config

BASE_URL =  config.url

def test_invalid_dm():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    remove_dm = requests.delete(f"{BASE_URL}/dm/remove/v1", json={
        'token': payload0['token'],
        'dm_id': 5,
    })

    assert remove_dm.status_code == 400


def test_auth_not_owner():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z2345678@gmail.com',
        'password': 'z2345678',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 =  user1.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z2345578@gmail.com',
        'password': 'z2345578',
        'name_first': 'Mochi',
        'name_last': 'Icecream'
    })
    payload2 =  user2.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm.json()

    remove_dm = requests.delete(f"{BASE_URL}/dm/remove/v1", json={
        'token': payload2['token'],
        'dm_id': payload3['dm_id']
    })

    assert remove_dm.status_code == 403

def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z2345678@gmail.com',
        'password': 'z2345678',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 =  user1.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    remove_dm = requests.delete(f"{BASE_URL}/dm/remove/v1", json={
        'token': payload0['token'] + 'abc',
        'dm_id': payload2['dm_id']
    })

    assert remove_dm.status_code == 403

def test_remove_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z2345678@gmail.com',
        'password': 'z2345678',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 =  user1.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    remove_dm = requests.delete(f"{BASE_URL}/dm/remove/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id']
    })

    dm_list = requests.get(f"{BASE_URL}/dm/list/v1?token={payload1['token']}")
    payload3 = dm_list.json()

    assert dm.status_code == 200
    assert remove_dm.status_code == 200
    assert dm_list.status_code == 200
    assert len(payload3['dms']) == 0



