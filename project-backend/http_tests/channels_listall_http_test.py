import requests
from src import config
BASE_URL =  config.url

def test_channels_list_all():
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

    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 2',
        'is_public': True
    })
    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload1['token'],
        'name': 'Test Channel 3',
        'is_public': True
    })
    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload1['token'],
        'name': 'Test Channel 4',
        'is_public': True
    })
    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload1['token'],
        'name': 'Test Channel 5',
        'is_public': True
    })

    listall = requests.get(f"{BASE_URL}/channels/listall/v2?token={payload0['token']}")


    assert listall.status_code == 200