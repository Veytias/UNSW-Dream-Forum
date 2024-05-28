import requests
from src import config
BASE_URL =  config.url

'''
server tests for message send functions
'''
'''
test 1: token invalid
'''
def test_message_send_token_invalid():

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'] + 'abc',
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })
    
    assert msgsend_resp.status_code == 403



'''
test 2: message send is too long
'''
def test_message_send_too_long():

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()


    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi"*666,
    })

    assert msgsend_resp.status_code == 400


'''
test 3: channel id invalid
'''

def test_message_send_cid_invalid():

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()


    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })


    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': -100,
        'message': "hi",
    })

    assert msgsend_resp.status_code == 403


'''
test 4: the user is not joined in the channel, raise AccessError
'''
def test_msgsend_user_not_joined():

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()


    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload1 = channelcreate_resp.json()

    register_resp2= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': '1234abcd',
        'name_first': 'Good',
        'name_last': 'Yo'
    })

    payload2 = register_resp2.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload2['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })

    assert msgsend_resp.status_code == 403

'''
test 5: msg send successful
'''

def test_message_send_success():
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })
    
    payload3 = msgsend_resp.json()

    assert msgsend_resp.status_code == 200
    assert payload3['message_id'] == 1

'''
test 6: user join channel, send message
'''
def test_user_send_message_joined():
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()


    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload1 = channelcreate_resp.json()

    register_resp2= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': '1234abcd',
        'name_first': 'Good',
        'name_last': 'Yo'
    })

    payload2 = register_resp2.json()

    requests.post(f"{BASE_URL}/channel/join/v2", json={
        'token': payload2['token'],
        'channel_id': payload1['channel_id'],
    })

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload2['token'],
        'channel_id': payload1['channel_id'],
        'message': "hi",
    })

    assert msgsend_resp.status_code == 200

'''
http tests for message_edit function
'''
def test_message_edit_token_invalid():
    '''
    token invalid
    '''
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload['token'] + 'abc',
        'message_id': payload3['message_id'],
        'message': "hi",
    })

    assert msgedit_resp.status_code == 403

def test_message_edit_mid_invalid_dm():
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register1_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5275107@gmail.com',
        'password': 'z5275107',
        'name_first': 'Suny',
        'name_last': 'So'
    })
    payload0 = register1_resp.json()

    register2_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload1 = register2_resp.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "hi",
    })

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload0['token'],
        'message_id': -5,
        'message': "hi",
    })

    assert msgedit_resp.status_code == 400

def test_message_edit_mid_invalid():
    '''
    token invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload['token'],
        'message_id': -5,
        'message': "hi",
    })

    assert msgedit_resp.status_code == 400

def test_message_edit_not_allowed():
    '''
    user has no authority to edit message
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    register_resp2= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': '1234abcd',
        'name_first': 'Good',
        'name_last': 'Yo'
    })
    payload4 = register_resp2.json()

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload4['token'],
        'message_id': payload3['message_id'],
        'message': "hey",
    })

    assert msgedit_resp.status_code == 403

def test_message_edit_not_allowed_dm():
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register1_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5275107@gmail.com',
        'password': 'z5275107',
        'name_first': 'Suny',
        'name_last': 'So'
    })
    payload0 = register1_resp.json()

    register2_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload1 = register2_resp.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    msg_senddm = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "hi",
    })
    payload3 = msg_senddm.json()

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload1['token'],
        'message_id': payload3['message_id'],
        'message': "hi",
    })

    assert msgedit_resp.status_code == 403

def test_edit_message_long():
    '''
    edit message long
    '''
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload['token'],
        'message_id': payload3['message_id'],
        'message': "hi"*666,
    })

    assert msgedit_resp.status_code == 400

def test_message_edit_not_exist():
    '''
    message to edit has been deleted
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    requests.delete(f"{BASE_URL}/message/remove/v1", json= {
        'token': payload['token'],
        'message_id': payload3['message_id'],
    })

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload['token'],
        'message_id': payload3['message_id'],
        'message': "hey",
    })

    assert msgedit_resp.status_code == 400

def test_message_edit_success():
    '''
    message_edit working properly
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload['token'],
        'message_id': payload3['message_id'],
        'message': "hey",
    })

    assert msgedit_resp.status_code == 200

def test_message_edit_success_dm():
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register1_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5275107@gmail.com',
        'password': 'z5275107',
        'name_first': 'Suny',
        'name_last': 'So'
    })
    payload0 = register1_resp.json()

    register2_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload1 = register2_resp.json()

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token':payload0['token'],
        'u_ids':[payload1['auth_user_id']]
    })
    payload2 = dm.json()

    msg_senddm = requests.post(f"{BASE_URL}message/senddm/v1", json={
        'token': payload0['token'],
        'dm_id': payload2['dm_id'],
        'message': "hi",
    })
    payload3 = msg_senddm.json()

    msgedit_resp = requests.put(f"{BASE_URL}/message/edit/v2", json={
        'token': payload0['token'],
        'message_id': payload3['message_id'],
        'message': "hi",
    })

    assert msgedit_resp.status_code == 200

'''
http tests for message_remove function
'''
def test_message_remove_token_invalid():
    '''
    token invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload['token'] + 'abc',
        'message_id': payload3['message_id'],
    })

    assert msgdelete_resp.status_code == 403

def test_message_delete_mid_invalid():
    '''
    message delete mid invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload['token'],
        'message_id': -5,
    })

    assert msgdelete_resp.status_code == 400


def test_message_delete_mid_invalid_dm():
    '''
    message delete mid invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload1 = register_resp.json()
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'happy@gmail.com',
        'password': 'woa999',
        'name_first': 'Suq',
        'name_last': 'Sa'
    })

    payload2 = register_resp.json()

    #create a dm
    dmcreate_resp = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload1['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })

    payload3 = dmcreate_resp.json()

    requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': payload1['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload1['token'],
        'message_id': -5,
    })

    assert msgdelete_resp.status_code == 400

def test_message_delete_mid_invalid_dm2():
    '''
    message delete mid invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload1 = register_resp.json()
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'happy@gmail.com',
        'password': 'woa999',
        'name_first': 'Suq',
        'name_last': 'Sa'
    })

    payload2 = register_resp.json()

    #create a dm
    dmcreate_resp = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload1['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })

    payload3 = dmcreate_resp.json()

    requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': payload1['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload1['token'],
        'message_id': None,
    })

    assert msgdelete_resp.status_code == 400   
    
def test_message_remove_not_allowed():
    '''
    user has no authority to remove message
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    register_resp2= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': '1234abcd',
        'name_first': 'Good',
        'name_last': 'Yo'
    })
    payload4 = register_resp2.json()

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload4['token'],
        'message_id': payload3['message_id'],
    })

    assert msgdelete_resp.status_code == 403

def test_message_remove_not_allowed_dm():
    '''
    user has no authority to remove message
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload1 = register_resp.json()
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'happy@gmail.com',
        'password': 'woa999',
        'name_first': 'Suq',
        'name_last': 'Sa'
    })

    payload2 = register_resp.json()

    #create a dm
    dmcreate_resp = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload1['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })

    payload3 = dmcreate_resp.json()

    senddm_resp = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': payload1['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })
    
    payload4 = senddm_resp.json()

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload2['token'],
        'message_id': payload4['message_id'],
    })

    assert msgdelete_resp.status_code == 403
    
def test_message_remove_not_exist():
    '''
    message to remove has been deleted
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    requests.delete(f"{BASE_URL}/message/remove/v1", json= {
        'token': payload['token'],
        'message_id': payload3['message_id'],
    })

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload['token'],
        'message_id': payload3['message_id'],
    })

    assert msgdelete_resp.status_code == 400


def test_message_remove_success():
    '''
    successful remove
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    #create a channel
    channelcreate_resp = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload['token'],
        'name': 'channelname1',
        'is_public': True,
    })

    payload2 = channelcreate_resp.json()

    msgsend_resp = requests.post(f"{BASE_URL}/message/send/v2", json={
        'token': payload['token'],
        'channel_id': payload2['channel_id'],
        'message': "hi",
    })

    payload3 = msgsend_resp.json()
    assert msgsend_resp.status_code == 200

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload['token'],
        'message_id': payload3['message_id'],
    })

    assert msgdelete_resp.status_code == 200

def test_message_remove_success_dm():
    '''
    successful remove
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload1 = register_resp.json()
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'happy@gmail.com',
        'password': 'woa999',
        'name_first': 'Suq',
        'name_last': 'Sa'
    })

    payload2 = register_resp.json()

    #create a dm
    dmcreate_resp = requests.post(f"{BASE_URL}/dm/create/v1", json={
        'token': payload1['token'],
        'u_ids':[payload1['auth_user_id'],payload2['auth_user_id']]
    })

    payload3 = dmcreate_resp.json()

    senddm_resp = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': payload1['token'],
        'dm_id': payload3['dm_id'],
        'message': "hi",
    })
    
    payload4 = senddm_resp.json()

    msgdelete_resp = requests.delete(f"{BASE_URL}/message/remove/v1", json={
        'token': payload1['token'],
        'message_id': payload4['message_id'],
    })

    assert msgdelete_resp.status_code == 200
