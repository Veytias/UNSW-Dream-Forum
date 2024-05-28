import pytest
from src.auth import auth_register_v2 as register
from src.message import message_send_v2 as message_send
from src.message import message_senddm_v1 as message_senddm
from src.message import message_react_v1 as message_react
from src.message import message_unreact_v1 as message_unreact
from src.message import message_edit_v2 as message_edit
from src.message import message_share_v1 as message_share
from src.channels import channels_create_v2 as channels_create
from src.channel import channel_invite_v2 as channel_invite
from src.channel import channel_addowner_v1 as channel_addowner
from src.dm import dm_create_v1 as dm_create
from src.dm import dm_invite_v1 as dm_invite
from src.helper import load_data, save_data
from src.notifications import notifications_get_v1 as notifications_get
from src.other import clear_v1 as clear
import src.error

def test_notifications_tag_message_send():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True)    
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    
    message_content = f"@jimapple hi"
    message_send(token1, channel_one_id, message_content)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': 1, 'dm_id': -1, 'notification_message': 'haydeneverest tagged you in channel_one: @jimapple hi'}
def test_notification_tag_message_senddm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_id = dm['dm_id']
    dm_name = dm['dm_name']
       
    message_content = "@jimapple hi"
    message_senddm(token1, dm_id, message_content)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': -1, 'dm_id': 1, 'notification_message': f'haydeneverest tagged you in {dm_name}: @jimapple hi'}
    
def test_notification_tag_message_edit_ch():
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
    message_new_content = "@jimapple hi"
    message_edit(token1, message['message_id'], message_new_content)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': 1, 'dm_id': -1, 'notification_message': 'haydeneverest tagged you in channel_one: @jimapple hi'}
    
def test_notification_tag_message_edit_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_id = dm['dm_id']
    dm_name = dm['dm_name']
       
    message_content = "@hi"
    message = message_senddm(token1, dm_id, message_content)
    message_new_content = "@jimapple hi"
    message_edit(token1, message['message_id'], message_new_content)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': -1, 'dm_id': 1, 'notification_message': f'haydeneverest tagged you in {dm_name}: @jimapple hi'}
def test_notification_tag_message_share_ch():
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
    message_new_content = "@jimapple"
    message_share(token1, message['message_id'], message_new_content, channel_one_id, -1)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': 1, 'dm_id': -1, 'notification_message': 'haydeneverest tagged you in channel_one: hi @jimapple'}
    
def test_notification_tag_message_share_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_id = dm['dm_id']
    dm_name = dm['dm_name']
       
    message_content = "hi"
    message = message_senddm(token1, dm_id, message_content)
    message_new_content = "@jimapple"
    message_share(token1, message['message_id'], message_new_content, -1, dm_id)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] == {'channel_id': -1, 'dm_id': 1, 'notification_message': f'haydeneverest tagged you in {dm_name}: hi @jimapple'}
    
def test_notification_tag_message_length():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True)    
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    
    message_content = "@jimapple Nooooooooooooooooooooooooooooooooooooooooooooooooo"
    limited_message = message_content[:20]
    message_send(token1, channel_one_id, message_content)
    notifs = notifications_get(token2)
    assert notifs['notifications'][1] ==  {'channel_id': 1, 'dm_id': -1, 'notification_message': f'haydeneverest tagged you in channel_one: {limited_message}'}
    
def test_notification_channel_invite():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True) 
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    notifs = notifications_get(token2)
    assert notifs['notifications'][0] == {'channel_id': 1,'dm_id': -1, 'notification_message': 'haydeneverest added you to channel_one'}

def test_notification_dm_invite():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', 'abcde123', 'Tom', 'Pear')
    
    token1 = user1['token'] 
    token3 = user3['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_id = dm['dm_id']
    dm_name = dm['dm_name']
    dm_invite(token1, dm_id, user3['auth_user_id'])
    notifs = notifications_get(token3)
    assert notifs['notifications'][0] == {'channel_id': -1,'dm_id': 1, 'notification_message': f'haydeneverest added you to {dm_name}'}
def test_notification_channel_addowner():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True) 
    channel_one_id = channel['channel_id']
    channel_addowner(token1, channel_one_id, user2['auth_user_id'])
    notifs = notifications_get(token2)
    assert notifs['notifications'][0] == {'channel_id': 1,'dm_id': -1, 'notification_message': 'haydeneverest added you to channel_one'}
def test_notification_dm_create():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_name = dm['dm_name']
    notifs = notifications_get(token2)
    assert notifs['notifications'][0] == {'channel_id': -1,'dm_id': 1, 'notification_message': f'haydeneverest added you to {dm_name}'}
def test_notification_react_ch():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True) 
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    message_content = "Good job!"
    message = message_send(token1, channel_one_id, message_content)
    message_react(token2, message['message_id'], 1)
    notifs = notifications_get(token1)
    assert notifs['notifications'][0] == {'channel_id': 1, 'dm_id': -1, 'notification_message': 'jimapple reacted to your message in channel_one'}
def test_notification_react_dm():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    dm = dm_create(token1, [user2['auth_user_id']]) 
    dm_id = dm['dm_id']
    dm_name = dm['dm_name']
       
    message_content = "Good job"
    message = message_senddm(token1, dm_id, message_content)
    message_react(token2, message['message_id'], 1)
    notifs = notifications_get(token1)
    assert notifs['notifications'][0] == {'channel_id': -1, 'dm_id': 1, 'notification_message': f'jimapple reacted to your message in {dm_name}'}
def test_most_recent_20_notifications():
    clear()
    user1 = register('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', 'abcde123', 'Jim', 'Apple')
    
    token1 = user1['token'] 
    token2 = user2['token']
    channel = channels_create(token1, 'channel_one', True) 
    channel_one_id = channel['channel_id']
    channel_invite(token1, channel_one_id, user2['auth_user_id'])
    message_content = "Good job!"
    message = message_send(token1, channel_one_id, message_content)
    for _ in range(50):
        message_react(token2, message['message_id'], 1)
        message_unreact(token2, message['message_id'], 1)
    notifs = notifications_get(token1)
    assert len(notifs['notifications']) == 20
