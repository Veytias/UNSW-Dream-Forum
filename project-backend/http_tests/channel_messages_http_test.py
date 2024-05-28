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
    
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload0['token']}&channel_id={'1'}&start={'0'}")
    assert message.status_code == 400

def test_channel_start_error(): 
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
        'name': 'Test Channel',
        'is_public': True
    })
    payload1 = channel.json()
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload0['token']}&channel_id={payload1['channel_id']}&start={'20'}")
    
    assert message.status_code == 400
    
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
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload2['token']}&channel_id={payload1['channel_id']}&start={'0'}")

    assert message.status_code == 403

def test_channel_message_success():
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
    requests.post(f"{BASE_URL}/message/send/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message':'hello'
    })
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload0['token']}&channel_id={payload1['channel_id']}&start={'0'}")
 
    payload2 = message.json()
    assert message.status_code == 200
    assert len(payload2['messages']) == 1
    assert payload2['messages'][0]['message'] == 'hello' 
    assert payload2['start'] == 0
    assert payload2['end'] == -1
    
def test_channel_multi_messages_success():
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
    requests.post(f"{BASE_URL}/message/send/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message':'hello'
    })
    requests.post(f"{BASE_URL}/message/send/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message':'hello'
    })
    requests.post(f"{BASE_URL}/message/send/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message':'hello'
    })
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload0['token']}&channel_id={payload1['channel_id']}&start={'0'}")
    
    payload2 = message.json()
    assert message.status_code == 200
    assert len(payload2['messages']) == 3
    assert payload2['start'] == 0
    assert payload2['end'] == -1
    
def test_channel_message_token_invalid():
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
    requests.post(f"{BASE_URL}/message/send/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'message':'hello'
    })
    message = requests.get(f"{BASE_URL}/channel/messages/v2?token={payload0['token']+'abc'}&channel_id={payload1['channel_id']}&start={'0'}")
    
    
    assert message.status_code == 403
