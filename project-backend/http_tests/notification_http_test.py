import requests
from src import config
BASE_URL =  config.url

def test_notifications_tag_message_send():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "@jackma hi",
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][1] == {'channel_id': 1,'dm_id': -1,'notification_message': 'sunnysun tagged you in channelname1: @jackma hi'}

   
def test_notification_tag_message_senddm():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload0['token'],
        'u_ids': [payload1['auth_user_id']],
    })
    payload2 = dm.json()
    requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "@jackma hi",
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][1] == {'channel_id': -1,'dm_id': 1,'notification_message': f"sunnysun tagged you in {payload2['dm_name']}: @jackma hi"}
def test_notification_tag_message_edit_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })
    payload3 = msg.json()
    requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload0['token'],
        'message_id': payload3['message_id'],
        'message': "@jackma hi",
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][1] == {'channel_id': 1,'dm_id': -1,'notification_message': 'sunnysun tagged you in channelname1: @jackma hi'}
def test_notification_tag_message_share_ch():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    msg = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })
    payload3 = msg.json()
    requests.post(f"{BASE_URL}/message/share/v1", json={
        'token': payload0['token'],
        'og_message_id': payload3['message_id'],
        'message': "@jackma",
        'channel_id': payload2['channel_id'],
        'dm_id': -1,
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload4 = notifs.json()
    assert notifs.status_code == 200
    assert payload4['notifications'][1] == {'channel_id': 1,'dm_id': -1,'notification_message': 'sunnysun tagged you in channelname1: hi @jackma'}
def test_notification_tag_message_length():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    message_content = "@jackma Nooooooooooooooooooooooooooooooooooooooooooooooooo"
    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload0['token'],
        'channel_id': payload2['channel_id'],
        'message': message_content,
    })
    limited_message = message_content[:20]
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][1] == {'channel_id': 1,'dm_id': -1,'notification_message': f'sunnysun tagged you in channelname1: {limited_message}'}
def test_notification_channel_invite():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/invite/v2", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][0] == {'channel_id': 1,'dm_id': -1,'notification_message': 'sunnysun added you to channelname1'}
    
def test_notification_dm_invite():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload0['token'],
        'u_ids': [payload1['auth_user_id']],
    })
    payload2 = dm.json()
    user3= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270709@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Chen'
    })
    payload3 = user3.json()
    requests.post(f"{BASE_URL}/dm/invite/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'u_id':payload3['auth_user_id'],
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload3['token']}")
    payload4 = notifs.json()
    assert notifs.status_code == 200
    assert payload4['notifications'][0] == {'channel_id': -1,'dm_id': 1,'notification_message': f"sunnysun added you to {payload2['dm_name']}"}
def test_notification_channel_addowner():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'channelname1',
        'is_public': True,
    })
    payload2 = channel.json()
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = {
        'token':payload0['token'],
        'channel_id': payload2['channel_id'],
        'u_id': payload1['auth_user_id'],
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][0] == {'channel_id': 1,'dm_id': -1,'notification_message': 'sunnysun added you to channelname1'}
def test_notification_dm_create():
    requests.delete(f"{BASE_URL}/clear/v1")
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload0 = user1.json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270708@gmail.com',
        'password': 'z5270707',
        'name_first': 'Jack',
        'name_last': 'Ma'
    })
    payload1 = user2.json()
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload0['token'],
        'u_ids': [payload1['auth_user_id']],
    })
    payload2 = dm.json()
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload1['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][0] == {'channel_id': -1,'dm_id': 1,'notification_message': f"sunnysun added you to {payload2['dm_name']}"}
def test_notification_react_ch():
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
    requests.post(f"{BASE_URL}/message/react/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
        'react_id' : 1,
    })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload0['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert payload3['notifications'][0] == {'channel_id': 1,'dm_id': -1,'notification_message': "sunnysun reacted to your message in channelname1"}
    
def test_most_recent_20_notifications():
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
    for _ in range(30):
        requests.post(f"{BASE_URL}/message/react/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
        'react_id' : 1,
        })
        requests.post(f"{BASE_URL}/message/unreact/v1", json = {
        'token': payload0['token'],
        'message_id': payload2['message_id'],
        'react_id' : 1,
        })
    notifs = requests.get(f"{BASE_URL}/notifications/get/v1?token={payload0['token']}")
    payload3 = notifs.json()
    assert notifs.status_code == 200
    assert len(payload3['notifications']) == 20
