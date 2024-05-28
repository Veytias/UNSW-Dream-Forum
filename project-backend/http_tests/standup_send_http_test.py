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

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload0['token'],
        'channel_id': 2,
        'message': 'Hi'
    })

    assert res.status_code == 400

def test_too_long_message():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    cha = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 2',
        'is_public': True
    })
    payload1 = cha.json()

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message' : 'A' * 1001
    })

    assert res.status_code == 400

def test_standup_is_not_running():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    cha = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 2',
        'is_public': True
    })
    payload1 = cha.json()

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message' : 'Hello'
    })

    assert res.status_code == 400

def test_authorised_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    cha = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 1',
        'is_public': True
    })
    payload2 = cha.json()

    requests.post(f"{BASE_URL}/standup/start/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'length': 1
    })

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Hi'
    })

    assert res.status_code == 403

def test_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 = user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    cha = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel 1',
        'is_public': True
    })
    payload2 = cha.json()

    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    requests.post(f"{BASE_URL}/standup/start/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'length': 1
    })

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Hi'
    })

    assert res.status_code == 200

    res = requests.post(f"{BASE_URL}/standup/send/v1", json = {
        'token':payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'Hello'
    })

    assert res.status_code == 200
