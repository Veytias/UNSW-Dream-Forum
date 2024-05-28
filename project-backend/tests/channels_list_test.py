import pytest
from src.auth import auth_register_v2 
from src.channel import channel_details_v2 
from src.channel import channel_join_v2 , channel_invite_v2
from src.channels import channels_create_v2 
from src.channels import channels_list_v2, channels_listall_v2 
from src.helper import getUserId, check_token_valid, load_data
from src.other import clear_v1
import src.error as error

def test_channels_list():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    user_id2 = auth_register_v2('second1email@gmail.com', '54321Hello', 'Dave', 'surname1')
    channels_create_v2(user_id1['token'],'name1', True)
    channel_create2 = channels_create_v2(user_id2['token'],'name2', True)
    channel_join_v2(user_id1['token'], channel_create2['channel_id'])
    assert channels_list_v2(user_id1['token']) == {
	    'channels': [{'channel_id' : 1, 'name' : 'name1'},{'channel_id' : 2, 'name' : 'name2'}]
	}


def test_channels_list_all():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    user_id2 = auth_register_v2('second1email@gmail.com', '54321Hello', 'Dave', 'surname1')
    ch_1 = channels_create_v2(user_id1['token'],'name1', True)
    ch_2 = channels_create_v2(user_id1['token'],'name2', False)
    ch_3 = channels_create_v2(user_id2['token'],'name3', False)
    ch_4 = channels_create_v2(user_id2['token'],'name4', True)
    ch_5 = channels_create_v2(user_id2['token'],'name5', False)

    expected_chs = [{'channel_id': ch_1['channel_id'], 'name' : 'name1'}, 
                    {'channel_id': ch_2['channel_id'], 'name' : 'name2'},
                    {'channel_id': ch_3['channel_id'], 'name' : 'name3'},
                    {'channel_id': ch_4['channel_id'], 'name' : 'name4'},
                    {'channel_id': ch_5['channel_id'], 'name' : 'name5'}]
    chs = channels_listall_v2(user_id1['token'])

    assert chs['channels'] == expected_chs

def test_when_one_channel_exites_private():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    ch_1 = channels_create_v2(user_id1['token'],'name1', False)

    channel_detail = {'channel_id': ch_1['channel_id'], 'name': 'name1'}
    channel_list = channels_listall_v2(user_id1['token'])

    assert channel_detail in channel_list['channels']

def test_when_one_channel_exists_public():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    ch_1 = channels_create_v2(user_id1['token'],'name1', True)

    channel_detail = {'channel_id': ch_1['channel_id'], 'name': 'name1'}
    channel_list = channels_listall_v2(user_id1['token'])

    assert channel_detail in channel_list['channels']

def test_channel_member_in_channel():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    user_id2 = auth_register_v2('second1email@gmail.com', '54321Hello', 'Dave', 'surname1')
    ch_1 = channels_create_v2(user_id1['token'],'name1', True)

    channel_invite_v2(user_id1['token'], ch_1['channel_id'], user_id2['auth_user_id'])

    expected = {'channel_id' : ch_1['channel_id'], 'name' : 'name1'}
    channel_list = channels_list_v2(user_id2['token'])

    assert expected in channel_list['channels']

def test_user_in_multiple_channels():
    clear_v1()
    user_id1 = auth_register_v2('first1email@gmail.com', '12345Hello', 'Josh', 'surname')
    ch_1 = channels_create_v2(user_id1['token'],'name1', False)
    ch_2 = channels_create_v2(user_id1['token'],'name2', False)

    expected_joined = [{'channel_id': ch_1['channel_id'], 'name': 'name1'}, {'channel_id': ch_2['channel_id'], 'name': 'name2'}]
    joined = channels_list_v2(user_id1['token'])

    assert expected_joined == joined['channels']

