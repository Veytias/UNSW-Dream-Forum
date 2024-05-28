#from pickle import load
import pytest
from src.auth import auth_register_v2 as register
from src.admin import userpermission
from src.other import clear_v1
from src.helper import load_data
#from src.user import user_profile_v2
import src.error

'''
InputError case
test 1 u_id does not refer to a valid user
'''
def test_u_id_invalid():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.InputError):
    #assume we do not have u_id 100 in database
        userpermission(user_1['token'], user_2['auth_user_id'], 1)
        userpermission(user_1['token'], 100, 1)

'''
The user is currently the only owner
'''
def test_permision_invalid():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.InputError):
        userpermission(user_1['token'],user_2['auth_user_id'], 3)

'''
AccessError case
test 1 The authorised user is not an owner.
'''
def test_auth_no_permisiion():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    with pytest.raises(src.error.AccessError):
        userpermission(user_2['token'],user_1['auth_user_id'], 2)

'''
Success 
'''
def test_userpermission_success():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","123456", "Steven", "Adam")
    userpermission(user_1['token'], user_2['auth_user_id'], 1)
    
    data = load_data()
    assert data['users'][user_2['auth_user_id']-1]['permission_id'] == 1

    userpermission(user_2['token'], user_1['auth_user_id'], 2)

    data = load_data()
    assert data['users'][user_1['auth_user_id']-1]['permission_id'] == 2
