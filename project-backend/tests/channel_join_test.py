import pytest
from src.channel import channel_join_v2
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
import src.error

#channel_join_v1(auth_user_id, channel_id)
def test_channel_id_invalid():
    clear_v1()
    user = auth_register_v2("channelidinvalid@gmail.com","a123456789","Micky","Mouse")
    with pytest.raises(src.error.InputError):
    #assume we do not have channel 100 in database
        channel_join_v2(user['token'],100)
    
    #clear_v1()
def test_channel_is_private():
    clear_v1()
    auth_user1 = auth_register_v2('testchannelprivate1@gmail.com','a123456789','tom','h0')
    auth_user2 = auth_register_v2('testchannelprivate2@gmail.com','a123456789','tom','h1')
    channel = channels_create_v2(auth_user1['token'],'channel_name',False)
    with pytest.raises(src.error.AccessError):
        #auth_user2 doesn't join channel yet.
        channel_join_v2(auth_user2['token'],channel['channel_id'])
    #clear_v1()
def test_join_success():
    clear_v1()
    auth_user1 = auth_register_v2('test1validemail@gmail.com','a123456789','tom','h')
    auth_user2 = auth_register_v2('test2validemail@gmail.com','b123456789','tom','h')
    new_channel = channels_create_v2(auth_user1['token'],'channelname',True)
    new_channel2 = channels_create_v2(auth_user1['token'],'channelname',True)
    channel_join_v2(auth_user2['token'],new_channel['channel_id'])
    channel_join_v2(auth_user2['token'],new_channel2['channel_id'])
    channel_index = new_channel['channel_id'] - 1 
    data = load_data()
    assert len(data['channels'][channel_index]['all_members']) == 2

def test_join_more_people_success():
    clear_v1()
    auth_user1 = auth_register_v2('test1validemail@gmail.com','a123456789','tom','h')
    auth_user2 = auth_register_v2('test2validemail@gmail.com','b123456789','tom','h')
    auth_user3 = auth_register_v2('test3validemail@gmail.com','b123456789','tom','h')
    auth_user4 = auth_register_v2('test4validemail@gmail.com','b123456789','tom','h')
    auth_user5 = auth_register_v2('test5validemail@gmail.com','b123456789','tom','h')
    new_channel = channels_create_v2(auth_user1['token'],'channelname',True)
    channel_join_v2(auth_user2['token'],new_channel['channel_id'])
    channel_join_v2(auth_user3['token'],new_channel['channel_id'])
    channel_join_v2(auth_user4['token'],new_channel['channel_id'])
    channel_join_v2(auth_user5['token'],new_channel['channel_id'])
    channel_index = new_channel['channel_id'] - 1 
    data = load_data()
    assert len(data['channels'][channel_index]['all_members']) == 5
    
    





