import pytest
from src.channel import channel_leave_v1,channel_join_v2
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
import src.error

def test_channel_id_invalid():
    clear_v1()
    user = auth_register_v2("channelidinvalid@gmail.com","a123456789","Micky","Mouse")
    with pytest.raises(src.error.InputError):
    #assume we do not have channel 100 in database
        channel_leave_v1(user['token'],100)

def test_user_not_in_channel():
    clear_v1()
    user1 = auth_register_v2("notinchannel1@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user1['token'],'name',True)
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    with pytest.raises(src.error.AccessError):
        channel_leave_v1(user2['token'],channel['channel_id'])

def test_user_leave_success():
    clear_v1()
    user1 = auth_register_v2("notinchannel1@gmail.com","a123456789","Micky","Mouse")
    channel = channels_create_v2(user1['token'],'name',True)
    channel2 = channels_create_v2(user1['token'],'name1',True)
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    user3 = auth_register_v2("notinchannel3@gmail.com","a123456789","Micky","Mouse3")
    channel_join_v2(user3['token'],channel2['channel_id'])
    channel_join_v2(user2['token'],channel['channel_id'])
    channel_join_v2(user3['token'],channel['channel_id'])
    channel_leave_v1(user3['token'],channel['channel_id'])
    data = load_data()
    in_channel = False
    for ch in data['users'][user3['auth_user_id']-1]['channels']:
        if channel['channel_id'] == ch['channel_id']:
            in_channel = True
    is_member = False
    for member in data['channels'][channel['channel_id']-1]['all_members']:
        if user3['auth_user_id'] == member['u_id']:
            is_member = True
    assert (in_channel == False and is_member == False)

