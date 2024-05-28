import pytest
from src.other import clear_v1 as clear
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_remove_v1
from src.helper import load_data
import src.error

'''
InputError cases
test 1 dm_id does not refer to an existing dm.
'''
def test_invalid_dm():   
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    token1 = user_id1['token']
    with pytest.raises(src.error.InputError):
        dm_remove_v1(token1, 5)

'''
AccessError cases
test 1 the authorised user is not original owner of dm.
'''
def test_auth_not_owner():
	
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    token2 = user_id2['token']
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    

    with pytest.raises(src.error.AccessError):
    	dm_remove_v1(token2, dm_create['dm_id'])

'''
test 2 invalid token
'''
def test_token_invalid():
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    token2 = user_id2['token']
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    

    with pytest.raises(src.error.AccessError):
    	dm_remove_v1(token2 + 'abc', dm_create['dm_id'])

def test_remove_success():
	
    clear()
    user_id1 = auth_register_v2('firstemail@gmail.com', '12345Hello', 'John', 'Snow')
    user_id2 = auth_register_v2('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')
    dm_create = dm_create_v1(user_id1['token'], [user_id2['auth_user_id']])
    dm_remove_v1(user_id1['token'], dm_create['dm_id'])
    data = load_data()

    assert len(data['dms']) == 0
