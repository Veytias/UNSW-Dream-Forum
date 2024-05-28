import requests
from src import config
BASE_URL =  config.url

def test_user_stats():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Channel1',
        'is_public': True
    })
    payload2 = channel1.json()

    dm1 = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm1.json()

    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })

    stat = requests.get(f"{BASE_URL}/user/stats/v1?token={payload0['token']}")

    assert stat.status_code == 200

def test_token_invalid():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    stat = requests.get(f"{BASE_URL}/user/stats/v1?token={payload0['token']+'abc'}")

    assert stat.status_code == 403

def test_users_stats():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z7654321@gmail.com',
        'password': 'z7654321',
        'name_first': 'Lion',
        'name_last': 'Bird'
    })
    payload1 = user2.json()

    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Channel1',
        'is_public': True
    })
    payload2 = channel1.json()

    dm1 = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload3 = dm1.json()

    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })

    stat = requests.get(f"{BASE_URL}/users/stats/v1?token={payload0['token']}")

    assert stat.status_code == 200

def test_token_invalid_dream():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Ant',
        'name_last': 'Man'
    })
    payload0 =  user.json()

    stat = requests.get(f"{BASE_URL}/users/stats/v1?token={payload0['token']+'abc'}")

    assert stat.status_code == 403
    

