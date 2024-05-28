import requests
from src import config
BASE_URL =  config.url


def test_channel_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    details = requests.get(f"{BASE_URL}/channel/details/v2?token={payload0['token']}&channel_id={'1'}")
    
    assert details.status_code == 400

def test_authorised_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload2 = user2.json()

    details = requests.get(f"{BASE_URL}/channel/details/v2?token={payload2['token']}&channel_id={payload1['channel_id']}")
    
    assert details.status_code == 403

def test_succesful_details():
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

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload2 = channel.json()
    
    requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
    })

    details = requests.get(f"{BASE_URL}/channel/details/v2?token={payload0['token']}&channel_id={payload2['channel_id']}")
    
    assert details.status_code == 200