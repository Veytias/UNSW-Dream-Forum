import requests
from src import config

BASE_URL =  config.url

def test_channel_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 =  user1.json()
    
    invite_ch = requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': 1,
        'u_id': payload1['auth_user_id'],
    })

    assert invite_ch.status_code == 400

def test_invalid_uid_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 = user.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()

    invite_ch = requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'u_id': 5,
    })

    assert invite_ch.status_code == 400

def test_token_invalid():
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

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload2 = channel.json()

    invite_ch = requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token': payload0['token'] + 'abc',
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    assert invite_ch.status_code == 403

def test_auth_user_channel():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234551@gmail.com',
        'password': 'z1234551',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 = user.json()

    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234569@gmail.com',
        'password': 'z1234569',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 = user1.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mochi',
        'name_last': 'Icecream'
    })
    payload2 = user2.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload3 = channel.json()

    invite_ch = requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token': payload1['token'],
        'channel_id': payload3['channel_id'],
        'u_id': payload2['auth_user_id'],
    })

    assert invite_ch.status_code == 403

def test_invite_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5123647@gmail.com',
        'password': 'z5123647',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 = user.json()

    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Rick',
        'name_last': 'Pickle'
    })
    payload1 = user1.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload2 = channel.json()

    invite_ch = requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    channel_info = requests.get(f"{BASE_URL}/channels/list/v2?token={payload1['token']}")
    
    payload3 = channel_info.json()

    assert invite_ch.status_code == 200
    assert channel_info.status_code == 200
    assert len(payload3['channels']) == 1
    
