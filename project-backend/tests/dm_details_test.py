import pytest
from src.auth import auth_register_v2 as register
from src.dm import dm_create_v1,dm_details_v1
from src.other import clear_v1
import src.error
import src.config as config

PORT = config.port
'''
InputError case
test 1 DM ID is not a valid DM.
'''
def test_dm_invalid():
    clear_v1()
    register("user_1@gmail.com","123456", "first_user_1", "last_user_1")
    user_2 = register("user_2@gmail.com","678901", "first_user_2", "last_user_2")
    with pytest.raises(src.error.InputError):
    #assume we do not have dm 1000 in database
        dm_details_v1(user_2['token'],1000)

'''
AccessError case
test 1 Authorised user is not a member of channel with channel_id.
'''
def test_dm_not_member():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "first_user_1", "last_user_1")
    user_2 = register("user_2@gmail.com","678901", "first_user_2", "last_user_2")
    user_3 = register("user_3@gmail.com","345678", "first_user_3", "last_user_3")
    user_4 = register("user_4@gmail.com","345678", "first_user_4", "last_user_4")
    dm = dm_create_v1(user_1['token'],[user_1['auth_user_id'],user_2['auth_user_id']])
    dm_create_v1(user_3['token'],[user_3['auth_user_id'],user_4['auth_user_id']])
    with pytest.raises(src.error.AccessError):
        dm_details_v1(user_3['token'],dm['dm_id'])
    

'''
Success case
'''

def test_succes_dm_details():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jack", "Smith")
    user_2 = register("user_2@gmail.com","678901", "Ant", "Jame")
    dm_create_v1(user_1['token'],[user_2['auth_user_id']])
    dm1 = dm_create_v1(user_1['token'],[user_2['auth_user_id']])


    detail = dm_details_v1(user_1['token'], dm1['dm_id'])

    print(detail)
    expected = {'name' : "antjame, jacksmith", 
                'members' : [{'email': 'user_1@gmail.com',
                            'handle_str': 'jacksmith',
                            'profile_img_url':f"http://localhost:{PORT}/static/initial.jpg",
                            'name_first': 'Jack',
                            'name_last': 'Smith',
                            'u_id': 1},
                            {'email': 'user_2@gmail.com',
                            'handle_str': 'antjame',
                            'profile_img_url':f"http://localhost:{PORT}/static/initial.jpg",
                            'name_first': 'Ant',
                            'name_last': 'Jame',
                            'u_id': 2}]}
    assert detail == expected
    
