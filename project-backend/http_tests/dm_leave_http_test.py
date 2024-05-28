import requests
from src import config
BASE_URL =  config.url

def test_dm_id_invalid():
    requests.delete(f'{BASE_URL}/clear/v1')
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    dm = requests.post(f"{BASE_URL}/dm/leave/v1", json={
         'token':payload0['token'],
         'dm_id':1})
    assert dm.status_code == 400
def test_user_not_in_dm():
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
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm.json()
    leave_status = requests.post(f"{BASE_URL}/dm/leave/v1", json={
         'token':payload2['token'],
         'dm_id':payload3['dm_id']})
    assert leave_status.status_code == 403
def test_user_leave_success():
    requests.delete(f'{BASE_URL}/clear/v1')
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
    leave_status = requests.post(f"{BASE_URL}/dm/leave/v1", json={
         'token':payload2['token'],
         'dm_id':payload3['dm_id']})
    dm_list = requests.get(f"{BASE_URL}/dm/list/v1?token={payload2['token']}")
    payload4 = dm_list.json()
    dm_list1 = requests.get(f"{BASE_URL}/dm/list/v1?token={payload1['token']}")
    payload5 = dm_list1.json() 
    assert leave_status.status_code == 200
    assert len(payload4['dms']) == 0
    assert len(payload5['dms']) == 1

def test_user_leave_token_invalid():
    requests.delete(f'{BASE_URL}/clear/v1')
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
    leave_status = requests.post(f"{BASE_URL}/dm/leave/v1", json={
         'token':payload2['token'] + "abc",
         'dm_id':payload3['dm_id']})
    
    assert leave_status.status_code == 403