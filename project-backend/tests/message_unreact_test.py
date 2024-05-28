import pytest
from src.message import message_send_v2 as message_send
from src.message import message_senddm_v1 as message_senddm
from src.message import message_react_v1 as message_react
from src.message import message_unreact_v1 as message_unreact
from src.channels import channels_create_v2 as channels_create
from src.channel import channel_invite_v2 as channel_invite
from src.channel import channel_messages_v2 as channel_messages
from src.dm import dm_messages_v1 as dm_messages
from src.dm import dm_create_v1 as dm_create
from src.helper import load_data
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
        message_unreact(token1, 2,1)
    
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
        message_unreact(token1, 2,1)
        
def test_invalid_react_id():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)

    with pytest.raises(src.error.InputError):
        message_unreact(token1, message['message_id'],2)
        
def test_not_reacted_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
   
    with pytest.raises(src.error.InputError):
        message_unreact(token1, message['message_id'],1)

def test_not_reacted_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
   
    with pytest.raises(src.error.InputError):
        message_unreact(token1, message['message_id'],1)
        
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
        message_unreact(token2, message['message_id'], 1)

def test_user_not_in_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']
    token2 = user3['token']
    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
    
    with pytest.raises(src.error.AccessError):
        message_unreact(token2, message['message_id'], 1)

def test_react_success_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token']
    token2 = user2['token']  
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    
    message_content = "hi"
    message = message_send(token1, channel_one_id, message_content)
   
    message_react(token2, message['message_id'], 1)
    message_unreact(token2, message['message_id'], 1)
    message_dict = channel_messages(token2, channel_one_id, 0)
    react = message_dict['messages'][0]['reacts'][0]
    assert react['react_id'] == 1
    assert react['u_ids'] == []
    assert react['is_this_user_reacted'] == False
    
def test_react_success_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']
    token2 = user2['token']

    dm = dm_create(token1, [user1['auth_user_id'],user2['auth_user_id']])
    dm_id = dm['dm_id']
    
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
   
    message_react(token2, message['message_id'], 1)
    message_unreact(token2, message['message_id'], 1)
    message_dict = dm_messages(token2, dm_id, 0)
    react = message_dict['messages'][0]['reacts'][0]
    assert react['react_id'] == 1
    assert react['u_ids'] == []
    assert react['is_this_user_reacted'] == False   