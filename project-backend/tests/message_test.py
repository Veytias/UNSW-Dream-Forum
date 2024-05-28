import pytest
from src.message import message_send_v2 as message_send
from src.message import message_remove_v1 as message_remove
from src.message import message_edit_v2 as message_edit
from src.channels import channels_create_v2 as channels_create
from src.channel import channel_join_v2 as channel_join
from src.auth import auth_register_v2 as register
from src.channel import channel_addowner_v1 as channel_addowner
from src.message import message_senddm_v1 as message_senddm
from src.dm import dm_create_v1 as dm_create
import src.error as error
from src.helper import load_data
from src.other import clear_v1 as clear

'''
tests for message send functions
'''

def test_message_too_long():
    '''
    Length of message is over 1000 characters, raise InputError
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    message_content = "hi"*666
    
    with pytest.raises(error.InputError):
        message_send(token1, channel_one_id, message_content)
        


def test_invalid_token():
    '''
    Token invalid, raise AccessError
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    message_content = "hi"
    
    with pytest.raises(error.AccessError):
        message_send(token1 + "abc", channel_one_id, message_content)
        

def test_invalid_channelid():
    '''
    channelid invalid, raise AccessError
    '''
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channels_create(token1, 'channel_one', True)
    message_content = "hi"
    
    with pytest.raises(error.AccessError):
        message_send(token1, -7, message_content)

def test_invalid_channelid_None():
    '''
    channelid invalid, raise AccessError
    '''
    clear()
    
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channels_create(token1, 'channel_one', True)
    message_content = "hi"
    
    with pytest.raises(error.AccessError):
        message_send(token1, None, message_content)
      

def test_user_not_joined():
    '''
    the user is not joined in the channel, raise AccessError
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    user2 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    token2 = user2['token']
    
    message_content = "hi"
    
    with pytest.raises(error.AccessError):
        message_send(token2, channel_one_id, message_content)
        
   

def test_message_send_success():
    '''
    success message send test case
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    assert message_id1['message_id'] == 1
        
  

def test_user_send_message_joined():
    '''
    the user joined in the channel, send message
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    user2 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    token2 = user2['token']
    channel_join(token2, channel_one_id)
    message_content = "hi"
    
    message_id1 = message_send(token2, channel_one_id, message_content)
    
    assert message_id1['message_id'] == 1



'''
tests for message_edit function
'''
def test_message_edit_token_invalid():
    '''
    token invalid
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.AccessError):
        message_edit(token1 + 'abc', message_id1['message_id'], "Hey u")



def test_message_edit_mid_invalid():
    '''
    message_id invalid
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.InputError):
        message_edit(token1, -3, "Hey u")

def test_message_edit_mid_invalid_dm():
    '''
    message_id invalid
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('valid@gmail.com', '12312de', 'Ha', 'Eve')
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_senddm(token1, dm_id1, message_content)
    
    with pytest.raises(error.InputError):
        message_edit(token1, -3, "Hey u")

def test_message_edit_not_allowed():
    '''
    user has no authority to edit
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token2 = user2['token']

    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.AccessError):
        message_edit(token2, message_id1['message_id'], "Hey u")

def test_message_edit_not_allowed_dm():
    '''
    user has no authority to edit
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_id1 = message_senddm(token1, dm_id1, message_content)
        
    token2 = user2['token']
    
    with pytest.raises(error.AccessError):
        message_edit(token2, message_id1['message_id'], "Hey u")
        
def test_message_edit_long():
    '''
    the edited message too long
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.InputError):
        message_edit(token1, message_id1['message_id'], 'h'*1001)

def test_message_edit_not_exist():
    '''
    message to edit has been deleted
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    message_remove(token1, message_id1['message_id'])
    
    with pytest.raises(error.InputError):
        message_edit(token1, message_id1['message_id'], "Hey")

def test_message_edit_success():
    '''
    message_edit working properly
    '''
    clear()
    data = load_data()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    message_content = "hello"
    message_send(token1, channel_one_id, message_content)

    message_edit(token1, message_id1['message_id'], "Hey")
    data = load_data()

    assert data['messages'][0]['message'] == "Hey"

    for msg in data['messages']:
        if msg['message_id'] == 1:
            assert msg['message'] == "Hey"


def test_message_edit_success_dm():
    '''
    message_edit working properly
    '''
    clear()
    data = load_data()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_senddm(token1, dm_id1, message_content)
    message_id1 = message_senddm(token1, dm_id1, message_content)
        
    
    message_edit(token1, message_id1['message_id'], "Hey")
    data = load_data()

    assert data['dms'][0]['messages'][1]['message'] == "Hey"
    
       

'''
tests for message_remove function
'''
def test_message_remove_token_invalid():
    '''
    token invalid
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.AccessError):
        message_remove(token1 + 'abc', message_id1['message_id'])



def test_message_remove_mid_invalid():
    '''
    message_id invalid
    '''

    clear()

    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.InputError):
        message_remove(token1, -3)
        
def test_message_remove_mid_invalid2():
    '''
    message_id invalid: empty
    '''

    clear()

    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.InputError):
        message_remove(token1, '')


def test_message_remove_not_allowed():
    '''
    user has no authority to remove
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token2 = user2['token']

    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(error.AccessError):
        message_remove(token2, message_id1['message_id'])




def test_message_remove_mid_invalid_dm():
    '''
    message_id invalid
    '''

    clear()

    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_senddm(token1, dm_id1, message_content)
        
    
    with pytest.raises(error.InputError):
        message_remove(token1, -3)
        
def test_message_remove_mid_invalid2_dm2():
    '''
    message_id invalid: empty
    '''

    clear()

    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_senddm(token1, dm_id1, message_content)
    
    with pytest.raises(error.InputError):
        message_remove(token1, '')


def test_message_remove_not_allowed_dm():
    '''
    user has no authority to remove
    '''
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hi"
    message_id1 = message_senddm(token1, dm_id1, message_content)
    token2 = user2['token']
    
    with pytest.raises(error.AccessError):
        message_remove(token2, message_id1['message_id'])


def test_message_remove_not_exist():
    '''
    message to remove has been deleted
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    message_remove(token1, message_id1['message_id'])
    
    with pytest.raises(error.InputError):
        message_remove(token1, message_id1['message_id'])

def test_message_remove_None():
    '''
    message to remove has been deleted
    '''

    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    channels_create(token1, 'channel_one', True)

    with pytest.raises(error.InputError):
        message_remove(token1, None)

def test_message_remove_success():
    '''
    message_remove working properly
    '''
    clear()
    data = load_data()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('valid2email@gmail.com', '1gfhfgcde', 'Barry', 'Allen')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    channel_addowner(token1, channel_one_id, user2['auth_user_id'])
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)
    message_id1 = message_send(token1, channel_one_id, message_content)

    message_remove(token2, message_id1['message_id'])
    assert data['messages'] == []

def test_message_remove_success_case2():
    '''
    message_remove working properly
    '''
    clear()
   
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('valid2email@gmail.com', '1gfhfgcde', 'Barry', 'Allen')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    channel_addowner(token1, channel_one_id, user2['auth_user_id'])
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    message_content = "hello"
    message_send(token1, channel_one_id, message_content)

    message_remove(token2, message_id1['message_id'])

    data = load_data()

    assert data['messages'][0]['message_id'] == 2
    assert len(data['messages']) == 1


def test_message_remove_success_case_dm():
    '''
    message_remove working properly
    '''
    clear()
   
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('valid2email@gmail.com', '1gfhfgcde', 'Barry', 'Allen')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user1['auth_user_id'], user2['auth_user_id']])
    dm_id1 = dm['dm_id']
    
    message_content = "hello"
    message_senddm(token2, dm_id1, message_content) 
    
    message_content = "hi"
    message_id1 = message_senddm(token1, dm_id1, message_content)
    
    message_remove(token1, message_id1['message_id'])
    
    data = load_data()

    assert len(data['dms'][0]['messages']) == 1
