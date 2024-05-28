import requests
from src import config

BASE_URL =  config.url

def test_invalid_channel():
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

    removeowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload0['token'],
        'channel_id': 1,
        'u_id': payload1['auth_user_id'],
    })

    assert removeowner_ch.status_code == 400

def test_not_owner():
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

    removeowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    assert removeowner_ch.status_code == 400

def test_only_owner():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()

    removeowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'u_id': payload0['auth_user_id'],
    })

    assert removeowner_ch.status_code == 400


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

    addowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload0['token'] + 'abc',
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    assert addowner_ch.status_code == 403

def test_auth_not_owner():
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
    payload3 = channel.json()

    removeowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload1['token'],
        'channel_id': payload3['channel_id'],
        'u_id': payload0['auth_user_id'],
    })

    assert removeowner_ch.status_code == 403

def test_removeowner_success():
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

    addowner_ch = requests.post(f"{BASE_URL}/channel/addowner/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })

    removeowner_ch = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = {
        'token':payload1['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload0['auth_user_id'],
    })

    details_ch = requests.get(f"{BASE_URL}/channel/details/v2?token={payload0['token']}&channel_id={payload2['channel_id']}")
    payload3 = details_ch.json()

    assert addowner_ch.status_code == 200
    assert removeowner_ch.status_code == 200
    assert details_ch.status_code == 200
    assert len(payload3['owner_members']) == 1