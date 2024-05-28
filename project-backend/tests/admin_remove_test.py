import pytest
from src.auth import auth_register_v2 as register
from src.admin import remove, userpermission
from src.other import clear_v1
from src.user import user_profile_v2
from src.message import message_send_v2
from src.helper import load_data, save_data
from src.channels import channels_create_v2
from src.channel import channel_join_v2
from src.channel import channel_invite_v2
from src.channel import channel_details_v2
from src.dm import dm_create_v1 as dm_create
from src.dm import dm_details_v1 as dm_details
import src.error

import src.config as config

PORT = config.port

'''
InputError case
test 1 u_id does not refer to a valid user
'''
def test_u_id_invalid():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.InputError):
    #assume we do not have u_id 100 in database
        remove(user_1['token'],100)


'''
The user is currently the only owner
'''
def test_only_user():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    with pytest.raises(src.error.InputError):
        remove(user_1['token'],user_1['auth_user_id'])

def test_one_dream_user():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.InputError):
        remove(user_1['token'],user_1['auth_user_id'])

'''
AccessError case
test 1 The authorised user is not an owner.
'''
def test_token_invalid():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    invalid_token = user_1['token'] + 'abc'
    with pytest.raises(src.error.AccessError):
        remove(invalid_token,user_2['auth_user_id'])

def test_auth_no_permisiion():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.AccessError):
        remove(user_2['token'],user_1['auth_user_id'])

'''
Success 
'''
def test_remove_success():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    channel = channels_create_v2(user_2['token'], 'channel_one', True)

    channel_one_id = channel['channel_id']
    
    userpermission(user_1['token'], user_2['auth_user_id'], 1)
    channel_invite_v2(user_2['token'], channel['channel_id'], user_1['auth_user_id'])
    message_content = "hi"
    message_content2 = "Sunday"
    message_send_v2(user_2['token'], channel_one_id, message_content)
    message_send_v2(user_2['token'], channel_one_id, message_content2)
    message_send_v2(user_1['token'], channel_one_id, message_content)


    remove(user_1['token'],user_2['auth_user_id'])

    profile = user_profile_v2(user_2['token'], user_2['auth_user_id'])

    expect_pro = {'user': {
            'u_id': user_2['auth_user_id'],
            'email': 'user_2@gmail.com',
            'name_first': 'Removed user',
            'name_last': 'Removed user',
            'handle_str': 'stevenadam',
            'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }}

    assert profile == expect_pro

    expect_msg = 'Removed user'
    data = load_data()

    for msg in data['messages']:
        if msg['u_id'] == user_2['auth_user_id']:
            assert msg['message'] == expect_msg  

def test_user_remove_from_channel():
    clear_v1()
    user_1 = register('user_1@gmail.com', '123456', 'Sam', 'Smith')
    user_2 = register('user_2@gmail.com', '678901', 'Bird', 'Nest')
    channel = channels_create_v2(user_1['token'], 'channel_one', True)
    channel_invite_v2(user_1['token'], channel['channel_id'], user_2['auth_user_id'])
    remove(user_1['token'],user_2['auth_user_id'])

    detail = channel_details_v2(user_1['token'], channel['channel_id'])

    assert detail['all_members'] == [{'u_id': user_1['auth_user_id'], 'name_first': 'Sam', 'name_last': 'Smith', 'email' : 'user_1@gmail.com','handle_str': 'samsmith', 'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg"}]
                                    
    members = detail['all_members']

    assert user_2['auth_user_id'] not in [m['u_id'] for m in members]

def test_user_remove_from_dm():
    clear_v1()
    user_1 = register('user_1@gmail.com', '123456', 'Sam', 'Smith')
    user_2 = register('user_2@gmail.com', '678901', 'Bird', 'Nest')
    dm = dm_create(user_1['token'],[user_2['auth_user_id']])
    remove(user_1['token'],user_2['auth_user_id'])
    detail = dm_details(user_1['token'], dm['dm_id'])

    members = detail['members']

    assert user_2['auth_user_id'] not in [m['u_id'] for m in members]

def test_user_remove_from_all_users():
    clear_v1()
    user_1 = register('user_1@gmail.com', '123456', 'Sam', 'Smith')
    user_2 = register('user_2@gmail.com', '678901', 'Bird', 'Nest')
    remove(user_1['token'],user_2['auth_user_id'])

    data = load_data()

    members = data['users']

    assert user_2['auth_user_id'] not in [m['u_id'] for m in members]
