import requests
from src import config
BASE_URL =  config.url

def test_invalid_message_id_within_channel():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload1 = channel.json()
    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    pin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload0['token'],
        'message_id': 2,
    })
    assert pin_stat.status_code == 400
def test_already_pinned_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload1 = channel.json()
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg.json()
    pin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
    })
    repin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
    })
    assert pin_stat.status_code == 200
    assert repin_stat.status_code == 400

def test_user_not_in_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload1 = channel.json()
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload3 = user2.json()
    pin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload3['token'],
        'message_id': payload2['message_id'],
    })
    assert pin_stat.status_code == 403
def test_user_not_owner_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload1 = channel.json()
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload3 = user2.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload1['channel_id'],
        'u_id': payload3['auth_user_id'],
    })
    pin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload3['token'],
        'message_id': payload2['message_id'],
    })
    assert pin_stat.status_code == 403
def test_pin_success_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload1 = channel.json()
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })
    payload2 = msg.json()
    pin_stat = requests.post(f"{BASE_URL}/message/pin/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
    })
    assert pin_stat.status_code == 200
