import pytest
from src.channel import channel_messages_v2
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_join_v2
from src.message import message_send_v2
from src.other import clear_v1
from src.helper import load_data, save_data
import src.error 

#channel_messages_v1(auth_user_id, channel_id, start)
def test_channel_id_invalid():
    clear_v1()
    user = auth_register_v2("channelidinvalid@gmail.com","a123456789","Micky","Mouse")
    with pytest.raises(src.error.InputError):
        channel_messages_v2(user['token'],15,0)

def test_channel_start_error():
    clear_v1()
    user = auth_register_v2("channelstarterror@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user['token'],'name',True)
    with pytest.raises(src.error.InputError):
        channel_messages_v2(user['token'],channel['channel_id'],50)

def test_user_not_in_channel():
    clear_v1()
    user1 = auth_register_v2("notinchannel1@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user1['token'],'name',True)
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    with pytest.raises(src.error.AccessError):
        channel_messages_v2(user2['token'],channel['channel_id'],0)
#I just add one new messages into messages dictionary for test use because we doesn't implementing Messages_create function in iteration 1
def test_channel_single_message_success():
    clear_v1()
    user1 = auth_register_v2("notinchannel@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user1['token'],'name',True)
    message_send_v2(user1['token'],channel['channel_id'],'Hello World')
    message = channel_messages_v2(user1['token'],channel['channel_id'],0)
    assert len(message['messages']) == 1
def test_channel_multiple_messages_success():
    clear_v1()
    user1 = auth_register_v2('testmessage@gmail.com','a123456789','tom','h')
    channel1 = channels_create_v2(user1['token'],'channelname1',True)
    channel2 = channels_create_v2(user1['token'],'channelname2',True)
    message_send_v2(user1['token'],channel1['channel_id'],'Hello World')
    for _ in range(100):    
        message_send_v2(user1['token'],channel2['channel_id'],'Hello World')
    message_send_v2(user1['token'],channel2['channel_id'],'Hello World')
    message = channel_messages_v2(user1['token'],channel2['channel_id'],0)
    assert len(message['messages']) == 50

def test_channel_messages_start_end():
    clear_v1()
    user1 = auth_register_v2("notinchannel@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user1['token'],'name',True)
    message_send_v2(user1['token'],channel['channel_id'],'Hello World')
    message = channel_messages_v2(user1['token'],channel['channel_id'],0)
    assert(message['start'] == 0 and message['end'] == -1)
