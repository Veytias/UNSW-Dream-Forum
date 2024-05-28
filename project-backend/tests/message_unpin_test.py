import pytest
from src.message import message_send_v2 as message_send
from src.message import message_senddm_v1 as message_senddm
from src.message import message_pin_v1 as message_pin
from src.message import message_unpin_v1 as message_unpin
from src.channels import channels_create_v2 as channels_create
from src.channel import channel_invite_v2 as channel_invite
from src.channel import channel_messages_v2 as channel_messages
from src.dm import dm_messages_v1 as dm_messages
from src.dm import dm_create_v1 as dm_create
#from src.helper import load_data
from src.other import clear_v1 as clear
from src.auth import auth_register_v2 as register
import src.error


def test_invalid_message_id_within_channel():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)
    
    with pytest.raises(src.error.InputError):
        message_unpin(token1, 2)
    
def test_invalid_message_id_within_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message_senddm(token1, dm_id, message_content)
    with pytest.raises(src.error.InputError):
        message_unpin(token1, 2)
        
        
def test_already_unpinned_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
    message_pin(token1, message['message_id'])
    message_unpin(token1, message['message_id'])
    with pytest.raises(src.error.InputError):
        message_unpin(token1, message['message_id'])

def test_already_unpinned_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
    message_pin(token1, message['message_id'])
    message_unpin(token1, message['message_id'])
    with pytest.raises(src.error.InputError):
        message_unpin(token1, message['message_id'])
def test_user_not_in_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']
    token2 = user2['token']  
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
    with pytest.raises(src.error.AccessError):
        message_unpin(token2, message['message_id'])

def test_user_not_in_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']    
    token3 = user3['token']
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
    with pytest.raises(src.error.AccessError):
        message_unpin(token3, message['message_id'])

def test_user_not_owner_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']
    token2 = user2['token']  
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    channel_invite(token1,channel_one_id, user2['auth_user_id'])
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
    with pytest.raises(src.error.AccessError):
        message_unpin(token2, message['message_id'])

def test_user_not_owner_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']
    token2 = user2['token']
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
    with pytest.raises(src.error.AccessError):
        message_unpin(token2, message['message_id'])
def test_pin_success_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
   
    message_pin(token1, message['message_id'])
    message_unpin(token1, message['message_id'])
    message_dict = channel_messages(token1, channel_one_id, 0)
    is_unpinned = message_dict['messages'][0]['is_pinned']
    assert is_unpinned == False

    
def test_unpin_success_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']

    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
   
    message_pin(token1, message['message_id'])
    message_unpin(token1, message['message_id'])
    message_dict = dm_messages(token1, dm_id, 0)
    is_unpinned = message_dict['messages'][0]['is_pinned']
    assert is_unpinned == False
