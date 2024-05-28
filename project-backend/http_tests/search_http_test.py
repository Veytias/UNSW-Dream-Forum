import requests
from src import config

BASE_URL =  config.url


def test_message_too_long():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    message = "hi" *666

    search = requests.get(f"{BASE_URL}/search/v2?token={payload0['token']}&query_str={message}")

    assert search.status_code == 400

def test_token_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Mickey',
        'name_last': 'Mouse'
    })
    payload0 =  user.json()

    message = "hi" 

    search = requests.get(f"{BASE_URL}/search/v2", json={
        'token': payload0['token'] + "abc",
        'query_str': message,
    })

    assert search.status_code == 403

def test_search_success_ch():
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

    msgsend1 = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "chocolate",
    })

    msgsend2 = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "chocolate mochi",
    })

    msgsend3 = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })

    search = requests.get(f"{BASE_URL}/search/v2?token={payload0['token']}&query_str={'chocolate'}")
    payload3 = search.json()

    assert msgsend1.status_code == 200
    assert msgsend2.status_code == 200
    assert msgsend3.status_code == 200
    assert search.status_code == 200
    assert len(payload3['messages']) == 2
   

def test_search_success_dm():
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

    msg_senddm1 = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "chocolate",
    })

    msg_senddm2 = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "chocolate mochi",
    })

    msg_senddm3 = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "hi",
    })

    search = requests.get(f"{BASE_URL}/search/v2?token={payload0['token']}&query_str={'chocolate'}")
    payload3 = search.json()

    assert msg_senddm1.status_code == 200
    assert msg_senddm2.status_code == 200
    assert msg_senddm3.status_code == 200
    assert search.status_code == 200
    assert len(payload3['messages']) == 2
