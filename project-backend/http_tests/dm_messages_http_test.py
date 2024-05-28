import requests
from src import config
BASE_URL =  config.url

def test_dm_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    dm = requests.get(f"{BASE_URL}/dm/messages/v1?token={payload0['token']}&dm_id={'1'}&start={'0'}")
    assert dm.status_code == 400
    
def test_dm_start_error():
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
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })
    payload3 = dm.json()
    messages = requests.get(f"{BASE_URL}/dm/messages/v1?token={payload0['token']}&dm_id={payload3['dm_id']}&start={'10'}")
    assert messages.status_code == 400
    
    
def test_user_not_in_dm():
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
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm.json()
    leave_status = requests.get(f"{BASE_URL}/dm/messages/v1?token={payload2['token']}&dm_id={payload3['dm_id']}&start={'0'}")
         
    assert leave_status.status_code == 403
    
def test_dm_single_message_success():
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
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })
    payload3 = dm.json()
    requests.post(f"{BASE_URL}/message/senddm/v1", json = {
        'token':payload0['token'],
        'dm_id': payload3['dm_id'],
        'message':'hello'
    })
    message_status = requests.get(f"{BASE_URL}/dm/messages/v1?token={payload0['token']}&dm_id={payload3['dm_id']}&start={'0'}")
    payload4 = message_status.json()
    assert message_status.status_code == 200
    assert len(payload4['messages']) == 1

def test_dm_single_message_token_invalid():
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
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z123456789@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload2 =  user3.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })
    payload3 = dm.json()
    requests.post(f"{BASE_URL}/message/senddm/v1", json = {
        'token':payload0['token'],
        'dm_id': payload3['dm_id'],
        'message':'hello'
    })
    message_status = requests.get(f"{BASE_URL}/dm/messages/v1?token={payload0['token']+'abc'}&dm_id={payload3['dm_id']}&start={'0'}")
         

    assert message_status.status_code == 403