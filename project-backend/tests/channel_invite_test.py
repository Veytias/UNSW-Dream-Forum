import pytest
from src.channel import channel_invite_v2
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1 as clear
from src.helper import load_data
import src.error
import src.config as config

PORT = config.port

'''
InputError cases
test 1 channel_id does not refer to a valid channel.
'''
def test_invalid_channel_id():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'Inviter', 'surname')
    auth_register_v2('secondemail@gmail.com', '54321Hello', 'Invitee', 'surname1')
    token1 = user_id1['token']
      
    with pytest.raises(src.error.InputError):
        channel_invite_v2(token1, 5, user_id1['auth_user_id'])
    
'''
test 2 u_id does not refer to a valid user.
'''
def test_invalid_uid_user():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'Inviter', 'surname')
    auth_register_v2('secondemail@gmail.com', '54321Hello', 'Invitee', 'surname1')
    token1 = user_id1['token']
    channel_create = channels_create_v2(token1,'name2', True)
    ch_id = channel_create['channel_id']
    
      
    with pytest.raises(src.error.InputError):
        channel_invite_v2(token1, ch_id, 9)

     
'''
AccessError cases
test 1 the authorised user is not already a member of the channel
'''
def test_auth_user_channel():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'Rick', 'Pickle')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mickey', 'Mouse')
    user_id3 = auth_register_v2('Thirdemail@gmail.com', '65a4s1df6', 'Jack', 'Sparrow')
    channel_create = channels_create_v2(user_id1['token'],'name3', True)
    ch_id = channel_create['channel_id']
    token2 = user_id2['token']
      
    with pytest.raises(src.error.AccessError):
        channel_invite_v2(token2, ch_id, user_id3['auth_user_id'])

'''
test 2 token invalid
'''
def test_token_invalid():
    clear()
    user_id1 = auth_register_v2('firstemail2@gmail.com', '12345Hello', 'Inviter', 'surname')
    user_id2 = auth_register_v2('secondemail2@gmail.com', '54321Hello', 'Invitee', 'surname1')
    channel_create = channels_create_v2(user_id1['token'], 'name3', True)
    ch_id = channel_create['channel_id']

    with pytest.raises(src.error.AccessError):
        channel_invite_v2(user_id1['token'] + "abc", ch_id, user_id2['auth_user_id'])

         
     
def test_invite_success():
    clear()
    user_id1 = auth_register_v2('firstemail3@gmail.com', '12345Hello', 'Inviter', 'surname')
    user_id2 = auth_register_v2('secondemail3@gmail.com', '54321Hello', 'Invitee', 'surname1')
    channel_create = channels_create_v2(user_id1['token'], 'name', True)

    channel_invite_v2(user_id1['token'], channel_create['channel_id'], user_id2['auth_user_id'])

    data = load_data()

    assert {'u_id': 2, 'name_first': 'Invitee', 'name_last': 'surname1', 'email' : 'secondemail3@gmail.com','handle_str': 'inviteesurname1', 'profile_img_url':f"http://localhost:{PORT}/static/initial.jpg"} == data['channels'][0]['all_members'][1]
    assert {'channel_id' : 1, 'name' : 'name'} == data['users'][1]['channels'][0]



