import pytest
from src.other import clear_v1 as clear
from src.auth import auth_register_v2
from src.dm import dm_invite_v1, dm_create_v1
from src.helper import load_data
import src.error
import src.config as config

PORT = config.port
'''
InputError cases
test 1 dm_id does not refer to an existing dm.
'''
def test_invalid_dm():
    
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    token1 = user_id1['token']
    
    with pytest.raises(src.error.InputError):
        dm_invite_v1(token1, 5, user_id2['auth_user_id'])

'''
test 2 u_id does not refer to a valid user.
'''
def test_invalid_uid():
    
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    token1 = user_id1['token']
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    dm_id = dm_create['dm_id']
    

    with pytest.raises(src.error.InputError):
        dm_invite_v1(token1, dm_id, 8)


'''
AccessError cases
test 1 the authorised user is not already a member of the dm.
'''
def test_dm_member():
    
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    user_id3 = auth_register_v2('thirdemail@gmail.com', '13579Hi', 'Mochi', 'icecream')
    token3 = user_id3['token']
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    dm_id = dm_create['dm_id']
    
    with pytest.raises(src.error.AccessError):
        dm_invite_v1(token3, dm_id, user_id1['auth_user_id'])

'''
test 2 token invalid
'''
def test_token_invalid():
    clear()
    user_id1 = auth_register_v2('firstemail2@gmail.com', '12345Hello', 'Inviter', 'surname')
    user_id2 = auth_register_v2('secondemail2@gmail.com', '54321Hello', 'Invitee', 'surname1')
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    dm_id = dm_create['dm_id']

    with pytest.raises(src.error.AccessError):
        dm_invite_v1(user_id1['token'] + "abc", dm_id, user_id2['auth_user_id'])


def test_success_invite():
    
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    user_id3 = auth_register_v2('thirdemail@gmail.com', '13579Hi', 'Mochi', 'icecream')
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    dm_invite_v1(user_id2['token'], dm_create['dm_id'], user_id3['auth_user_id'])

    data = load_data()
    
    assert {'u_id': 3, 'name_first': 'Mochi', 'name_last': 'icecream', 'email': 'thirdemail@gmail.com', 'handle_str': 'mochiicecream', 'profile_img_url':f"http://localhost:{PORT}/static/initial.jpg"} == data['dms'][0]['dm_members'][2]
