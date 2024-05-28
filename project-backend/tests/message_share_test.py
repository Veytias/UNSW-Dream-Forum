import pytest
from src.message import message_send_v2 as message_send
from src.message import message_senddm_v1 as message_senddm
from src.message import message_share_v1
from src.channels import channels_create_v2 as channels_create
from src.dm import dm_create_v1
#from src.helper import load_data
from src.other import clear_v1 as clear
from src.auth import auth_register_v2 as register
import src.error

'''
Inputerror, og_message_id does not refer to a message
'''
def test_og_message_invalid_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)

    add_message = 'lol'

    with pytest.raises(src.error.InputError):
        message_share_v1(token1, -5, add_message, channel_one_id, -1)

def test_og_message_invalid_ch_None():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_send(token1, channel_one_id, message_content)

    add_message = 'lol'

    with pytest.raises(src.error.InputError):
        message_share_v1(token1, None, add_message, channel_one_id, -1)

def test_og_message_invalid_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    dm = dm_create_v1(token1, [user2['auth_user_id']])
    
    message_content = "hi"
    message_senddm(token1, dm['dm_id'], message_content)

    add_message = 'lol'

    with pytest.raises(src.error.InputError):
        message_share_v1(token1, -5, add_message, -1, dm['dm_id'])

def test_og_message_invalid_dm_None():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    dm = dm_create_v1(token1, [user2['auth_user_id']])
    
    message_content = "hi"
    message_senddm(token1, dm['dm_id'], message_content)

    add_message = 'lol'

    with pytest.raises(src.error.InputError):
        message_share_v1(token1, None, add_message, -1, dm['dm_id'])

'''
Accesserror, authorised user has not joined the channel or DM they are trying to share the message to
'''
def test_user_not_member_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']
    token2 = user2['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    add_message = 'lol'

    with pytest.raises(src.error.AccessError):
        message_share_v1(token2, message_id1['message_id'], add_message, channel_one_id, -1)

def test_user_not_member_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', 'asf512sa', 'Rick', 'Pickle')

    token1 = user1['token']
    user2['token']
    token3 = user3['token']
    dm = dm_create_v1(token1, [user2['auth_user_id']])
    
    message_content = "hi"
    message_id1 = message_senddm(token1, dm['dm_id'], message_content)

    add_message = 'lol'

    with pytest.raises(src.error.AccessError):
        message_share_v1(token3, message_id1['message_id'], add_message, -1, dm['dm_id'])

'''
test 2 invalid token
'''
def test_token_invalid():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']
    user2['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    add_message = 'lol'
    
    with pytest.raises(src.error.AccessError):
        message_share_v1(token1 + "abc" , message_id1['message_id'], add_message, channel_one_id, -1)
        

def test_share_success_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']
    user2['token'] 
    channel = channels_create(token1, 'channel_one', True)
    channel_one_id = channel['channel_id']
    
    message_content = "hi"
    message_id1 = message_send(token1, channel_one_id, message_content)

    add_message = 'lol'

    share_message1 = message_share_v1(token1, message_id1['message_id'], add_message, channel_one_id, -1)
    
    
    assert share_message1['shared_message_id'] == 2
    

def test_share_success_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')

    token1 = user1['token']
    token2 = user2['token']
    dm_create_v1(token1, [user2['auth_user_id']])
    dm = dm_create_v1(token1, [user2['auth_user_id']])
    dm_create_v1(token2, [user1['auth_user_id']])

    
    message_content = "hi"
    message_senddm(token1, dm['dm_id'], message_content)
    message_id1 = message_senddm(token1, dm['dm_id'], message_content)
    

    add_message = 'lol'

    
    share_message2 = message_share_v1(token2, message_id1['message_id'], add_message, -1, dm['dm_id'])
    
    
    assert share_message2['shared_message_id'] == 3
    

        


