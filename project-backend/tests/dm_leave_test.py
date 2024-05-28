import pytest
from src.auth import auth_register_v2
from src.dm import dm_create_v1,dm_leave_v1
from src.other import clear_v1
from src.helper import load_data
import src.error

def test_dm_id_invalid():
    clear_v1()
    user = auth_register_v2("channelidinvalid@gmail.com","a123456789","Micky","Mouse")
    with pytest.raises(src.error.InputError):
    #assume we do not have dm 100 in database
        dm_leave_v1(user['token'],100)

def test_user_not_in_dm():
    clear_v1()
    user1 = auth_register_v2("notinchannel1@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    user3 = auth_register_v2("notinchannel3@gmail.com","a123456789","Micky","Mouse3")
    dm = dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    with pytest.raises(src.error.AccessError):
        dm_leave_v1(user3['token'],dm['dm_id'])

def test_user_leave_success():
    clear_v1()
    user1 = auth_register_v2("notinchannel1@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    user3 = auth_register_v2("notinchannel3@gmail.com","a123456789","Micky","Mouse3")
    dm_create_v1(user1['token'],[user2['auth_user_id'],user3['auth_user_id']])
    dm2 = dm_create_v1(user1['token'],[user2['auth_user_id'],user3['auth_user_id']])
    dm_leave_v1(user3['token'],dm2['dm_id'])
    data = load_data()
    in_dm = False
    
    for dm_var in data['dms'][dm2['dm_id']-1]['dm_members']:
        if dm_var['u_id'] == user3['auth_user_id']:
            in_dm = True
   
    assert (in_dm == False)
