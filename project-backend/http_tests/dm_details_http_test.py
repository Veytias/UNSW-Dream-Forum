import requests
from src import config
BASE_URL =  config.url
    
def test_dm_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    dm_details = requests.get(f"{BASE_URL}/dm/details/v1?token={payload1['token']}&dm_id={'100'}")
    
    assert dm_details.status_code == 400

def test_dm_not_member():
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

    user4 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z9887664@gmail.com',
        'password': 'z9887664',
        'name_first': 'King',
        'name_last': 'Shark'
    })
    payload3 = user4.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload4 = dm.json()

    requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload2['token'],
        'u_ids':[payload3['auth_user_id']]
    })

    dm_details = requests.get(f"{BASE_URL}/dm/details/v1?token={payload2['token']}&dm_id={payload4['dm_id']}")
       
    
    assert dm_details.status_code == 403

def test_succes_dm_details():
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    dm_details = requests.get(f"{BASE_URL}/dm/details/v1?token={payload0['token']}&dm_id={payload2['dm_id']}")
    
    assert dm_details.status_code == 200


