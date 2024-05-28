import requests
from src import config
BASE_URL =  config.url

def test_invalid_channel():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 2',
        'is_public': True
    })

    res = requests.get(f"{BASE_URL}/standup/active/v1", json = {
        'token':payload0['token'],
        'channel_id': 2
    })

    res = requests.get(f"{BASE_URL}/standup/active/v1?token={payload0['token']}&channel_id={'2'}")

    assert res.status_code == 400

def test_success_active():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    cha = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Channel_1',
        'is_public': True
    })
    payload1 = cha.json()

    requests.post(f"{BASE_URL}/standup/start/v1", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'length': 2
    })

    res = requests.get(f"{BASE_URL}/standup/active/v1?token={payload0['token']}&channel_id={payload1['channel_id']}")

    assert res.status_code == 200

