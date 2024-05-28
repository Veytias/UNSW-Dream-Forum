import requests
from src import config
BASE_URL =  config.url

def test_channel_name_too_long():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'zxcvbnmasdfghjklqwertyuiopoi',
        'is_public': True
    })
    assert channel.status_code == 400
    
def test_channels_create_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Nintendo Online',
        'is_public': True
    })
    payload1 = channel.json()
    assert channel.status_code == 200
    assert payload1 == {'channel_id': 1}
    
def test_channels_create_info():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Nintendo Online',
        'is_public': True
    })
    channel_info = requests.get(f"{BASE_URL}/channels/list/v2?token={payload0['token']}")

    payload1 = channel.json()
    payload2 = channel_info.json()
  
    assert channel.status_code == 200
    assert channel_info.status_code == 200
    assert payload1['channel_id'] == payload2['channels'][payload1['channel_id'] - 1]['channel_id']
    assert payload2['channels'][payload1['channel_id'] - 1]['name'] == 'Nintendo Online'

def test_channels_create_token_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'] + "abc",
        'name': 'Nintendo Online',
        'is_public': True
    })
    
    assert channel.status_code == 403