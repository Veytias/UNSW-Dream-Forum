import requests
from src import config
BASE_URL =  config.url

def test_dm_invalid_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload1 =  user2.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id'],3]
    })
    assert dm.status_code == 400

def test_dm_create_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload1 =  user2.json()
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })
    payload3 = dm.json()
    dm_list = requests.get(f"{BASE_URL}/dm/list/v1?token={payload0['token']}")
    payload4 = dm_list.json()
    assert dm.status_code == 200
    assert payload3 == { 'dm_id':1,
                         'dm_name':"nintendoswitch, nintendoswitch0, nintendoswitch1"}
    assert payload4['dms'][0] ==  { 'dm_id':1, 
                                    'name':"nintendoswitch, nintendoswitch0, nintendoswitch1"
    }

def test_dm_create_token_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload1 =  user2.json()
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'] + "abc",
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })
    
    assert dm.status_code == 403
