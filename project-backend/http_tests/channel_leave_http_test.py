import requests
from src import config

BASE_URL =  config.url

def test_leavechannel_token_invalid():
	
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 = user2.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload2['token'],
        'channel_id': payload1['channel_id'],
    })
    leave_ch = requests.post(f"{BASE_URL}/channel/leave/v1", json = {
        'token':payload2['token'] + "abc",
        'channel_id': payload1['channel_id'],
    })
    
    
    assert join_ch.status_code == 200
    assert leave_ch.status_code  == 403
    
def test_channel_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    leave_ch = requests.post(f"{BASE_URL}/channel/leave/v1", json = {
        'token':payload0['token'],
        'channel_id': 1,
    })
    assert leave_ch.status_code == 400
    
def test_user_not_in_channel():    
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 = user2.json()
    leave_ch = requests.post(f"{BASE_URL}/channel/leave/v1", json = {
        'token':payload2['token'],
        'channel_id': payload1['channel_id'],
    })
    assert leave_ch.status_code == 403
    
def test_user_leave_success():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user1.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z12345678@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 = user2.json()
    join_ch = requests.post(f"{BASE_URL}/channel/join/v2", json = {
        'token':payload2['token'],
        'channel_id': payload1['channel_id'],
    })
    leave_ch = requests.post(f"{BASE_URL}/channel/leave/v1", json = {
        'token':payload2['token'],
        'channel_id': payload1['channel_id'],
    })
    channel_info = requests.get(f"{BASE_URL}/channels/list/v2?token={payload2['token']}")
    payload3 = channel_info.json()
    
    assert join_ch.status_code == 200
    assert leave_ch.status_code  == 200
    assert channel_info.status_code == 200
    assert len(payload3['channels']) == 0
