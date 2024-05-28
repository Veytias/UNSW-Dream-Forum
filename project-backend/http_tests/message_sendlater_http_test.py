import requests
from src import config

BASE_URL =  config.url

'''
message_sendlater test
'''

def test_invalid_channelid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload0['token'],
        'channel_id': -5,
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlater.status_code == 400


def test_message_too_long():
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

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': 'hi'*666,
        'time_sent': 10
    })

    assert msg_sendlater.status_code == 400

def test_time_past():
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

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': 'hi',
        'time_sent': -10
    })

    assert msg_sendlater.status_code == 400

def test_token_invalid():
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

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload0['token']+ "abc",
        'channel_id': payload1['channel_id'],
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlater.status_code == 403

def test_not_member_ch():
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

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload1['token'],
        'channel_id': payload2['channel_id'],
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlater.status_code == 403

def test_sendlater_success():
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

    msg_sendlater = requests.post(f"{BASE_URL}/message/sendlater/v1", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': 'hi',
        'time_sent': 5
    })
    payload2 = msg_sendlater.json()

    assert msg_sendlater.status_code == 200
    assert payload2['message_id'] == 1


'''
message_sendlaterdm_test
'''
def test_invalid_dmid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload0['token'],
        'dm_id': -5,
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlaterdm.status_code == 400


def test_message_too_long_dm():
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': 'hi'*666,
        'time_sent': 10
    })

    assert msg_sendlaterdm.status_code == 400

def test_time_past_dm():
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': 'hi',
        'time_sent': -10
    })

    assert msg_sendlaterdm.status_code == 400

def test_token_invalid_dm():
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload0['token'] + "abc",
        'dm_id': payload2['dm_id'],
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlaterdm.status_code == 403

def test_not_member_dm():
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

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z2345578@gmail.com',
        'password': 'z2345578',
        'name_first': 'Mochi',
        'name_last': 'Icecream'
    })
    payload2 =  user2.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm.json()

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload2['token'],
        'dm_id': payload3['dm_id'],
        'message': 'hi',
        'time_sent': 10
    })

    assert msg_sendlaterdm.status_code == 403

def test_sendlaterdm_success():
    requests.delete(f"{BASE_URL}/clear/v1")
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "hii",
    })

    msg_sendlaterdm = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': 'hi',
        'time_sent': 5
    })
    payload3 = msg_sendlaterdm.json()


    assert msg_sendlaterdm.status_code == 200
    assert payload3['message_id'] == 2
    


