import requests
from src import config
BASE_URL =  config.url

def test_succes_dm_list():
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
    payload1 = user2.json()

    requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })


    dm_list = requests.get(f"{BASE_URL}/dm/list/v1?token={payload0['token']}")

    assert dm_list.status_code == 200

def test_user_in_multi_dm():
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
    payload1 = user2.json()

    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234432@gmail.com',
        'password': 'z1234432',
        'name_first': 'Snake',
        'name_last': 'Eyes'
    })
    payload2 = user3.json()

    requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload2['token'],
        'u_ids':[payload1['auth_user_id']]
    })

    dm_lists = requests.get(f"{BASE_URL}/dm/list/v1?token={payload0['token']}")
    
    assert dm_lists.status_code == 200