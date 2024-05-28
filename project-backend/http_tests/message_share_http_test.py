import requests
from src import config

BASE_URL =  config.url

def test_og_message_invalid_ch():
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

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload0['token'],
        'og_message_id': 5,
        'message': "Hello",
        'channel_id': payload1['channel_id'],
        'dm_id': -1,
    })

    assert msg_share.status_code == 400

def test_user_not_member_ch():
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

    msgsend = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })
    payload3 = msgsend.json()

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': "Hello",
        'channel_id': payload2['channel_id'],
        'dm_id': -1,
    })

    assert msg_share.status_code == 403

def test_user_not_member_dm():
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

    msg_senddm = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })
    payload4 = msg_senddm.json()

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload2['token'],
        'og_message_id': payload4['message_id'],
        'message': "Hello",
        'channel_id': -1,
        'dm_id': payload3['dm_id'],
    })

    assert msg_share.status_code == 403

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

    msg_send = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg_send.json()

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload0['token'] + "abc",
        'og_message_id': payload2['message_id'],
        'message': "Hello",
        'channel_id': payload1['channel_id'],
        'dm_id': -1,
    })

    assert msg_share.status_code == 403

def test_share_success_ch():
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

    msg_send = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg_send.json()

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload0['token'],
        'og_message_id': payload2['message_id'],
        'message': "Hello",
        'channel_id': payload1['channel_id'],
        'dm_id': -1,
    })
    payload4 = msg_share.json()

    assert msg_share.status_code == 200
    assert payload4['shared_message_id'] == 2

def test_share_success_dm():
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

    msg_senddm = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload1['token'],
        'dm_id': payload2['dm_id'],
        'message': "hi",
    })
    payload3 = msg_senddm.json()

    msg_share = requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload1['token'],
        'og_message_id': payload3['message_id'],
        'message': "Hello",
        'channel_id': -1,
        'dm_id': payload2['dm_id'],
    })
    payload4 = msg_share.json()

    assert msg_share.status_code == 200
    assert payload3['message_id'] == 1
    assert payload4['shared_message_id'] == 2

    
