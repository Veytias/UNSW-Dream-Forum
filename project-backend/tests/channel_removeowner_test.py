import pytest
from src.channel import channel_addowner_v1, channel_removeowner_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.helper import load_data
from src.other import clear_v1 as clear
import src.error

'''
InputError cases
test1 channel_id does not refer to a valid channel
'''
def test_invalid_channel():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
      
    with pytest.raises(src.error.InputError):
        channel_removeowner_v1(user_id1['token'], 5, user_id2['auth_user_id'])

'''
test2 user with user id u_id is not an owner of the channel
'''
def test_notowner():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    channel_create = channels_create_v2(user_id1['token'],'name2', True)
    

    with pytest.raises(src.error.InputError):
        channel_removeowner_v1(user_id1['token'], channel_create['channel_id'], user_id2['auth_user_id'])

'''
test3 user is currently the only owner
'''
def test_onlyowner():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    channel_create = channels_create_v2(user_id1['token'],'name2', True)

    with pytest.raises(src.error.InputError):
        channel_removeowner_v1(user_id1['token'], channel_create['channel_id'], user_id1['auth_user_id'])

'''
AccessError case
test1 Authorized user is not an owner of the channel
'''
def test_auth_notowner():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    
    channel_create = channels_create_v2(user_id1['token'],'name2', True)
      
    with pytest.raises(src.error.AccessError):
        channel_removeowner_v1(user_id2['token'], channel_create['channel_id'], user_id1['auth_user_id'])

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
        channel_removeowner_v1(user_id1['token'] + "abc", ch_id, user_id2['auth_user_id'])

def test_remove_success():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    user_id3 = auth_register_v2('Thirdemail@gmail.com', '54asdHello', 'Barry', 'Allen')
    channel_create = channels_create_v2(user_id1['token'],'name2', True)
    channel_addowner_v1(user_id1['token'], channel_create['channel_id'], user_id2['auth_user_id'])
    channel_addowner_v1(user_id1['token'], channel_create['channel_id'], user_id3['auth_user_id'])
    channel_removeowner_v1(user_id2['token'], channel_create['channel_id'], user_id3['auth_user_id'])

    data = load_data()

    assert len(data['channels'][0]['owner_members']) == 2
