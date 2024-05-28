import requests
from src import config

BASE_URL =  config.url
    
def test_channel_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload0['token'],
        'channel_id': 1,
    })
    assert join_ch.status_code == 400
    
def test_channel_is_private():
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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': False
    })
    payload2 = channel.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload1['token'],
        'channel_id': payload2['channel_id'],
    })
    assert join_ch.status_code == 403
    
def test_join_success():
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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload2 = channel.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload1['token'],
        'channel_id': payload2['channel_id'],
    })
    channel_info = requests.get(f"{BASE_URL}/channels/list/v2?token={payload1['token']}")
    
    payload3 = channel_info.json()

    assert join_ch.status_code == 200
    assert channel_info.status_code == 200
    assert payload3['channels'][0]['channel_id'] == payload2['channel_id']
    assert payload3['channels'][0]['name'] == 'Test Channel'

def test_join_token_invalid():
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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload2 = channel.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload1['token'] + "abc",
        'channel_id': payload2['channel_id'],
    })
    

    assert join_ch.status_code == 403
    
