import pytest
import src.channel
from src.auth import auth_register_v2
#from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.helper import load_data
import src.error


def test_dm_invalid_user():
    clear_v1()
    auth_user1 = auth_register_v2('testdminvaliduser1@gmail.com','a123456789','tom','h0')
    auth_user2 = auth_register_v2('testdminvaliduser2@gmail.com','a123456789','tom','h1')
    with pytest.raises(src.error.InputError):
        dm_create_v1(auth_user1['token'],[auth_user2['auth_user_id'],3])

def test_dm_create_success():
    clear_v1()  
    auth_user1 = auth_register_v2('testdmcreatesuccess1@gmail.com','a123456789','tom','h0')
    auth_user2 = auth_register_v2('testdmcreatesuccess2@gmail.com','a123456789','tom','h0')
    auth_user3 = auth_register_v2('testdmcreatesuccess3@gmail.com','a123456789','tom','h0')
    dm_create_v1(auth_user1['token'],[auth_user2['auth_user_id'],auth_user3['auth_user_id']])
    data = load_data()
    assert (len(data['dms']) == 1)

def test_more_dm_create_success():
    clear_v1()  
    auth_user1 = auth_register_v2('testdmcreatesuccess1@gmail.com','a123456789','tom','h0')
    auth_user2 = auth_register_v2('testdmcreatesuccess2@gmail.com','a123456789','tom','h0')
    auth_user3 = auth_register_v2('testdmcreatesuccess3@gmail.com','a123456789','tom','h0')
    dm_create_v1(auth_user1['token'],[auth_user2['auth_user_id'],auth_user3['auth_user_id']])
    dm_create_v1(auth_user2['token'],[auth_user1['auth_user_id'],auth_user3['auth_user_id']])
    dm_create_v1(auth_user3['token'],[auth_user1['auth_user_id'],auth_user2['auth_user_id']])
    data = load_data()
    assert (len(data['dms']) == 3)   
def test_dm_name_sort():
    clear_v1()  
    auth_user1 = auth_register_v2('testdmcreatesuccess1@gmail.com','a123456789','tom','h2')
    auth_user2 = auth_register_v2('testdmcreatesuccess2@gmail.com','a123456789','tom','h1')
    auth_user3 = auth_register_v2('testdmcreatesuccess3@gmail.com','a123456789','tom','h0')
    dm = dm_create_v1(auth_user1['token'],[auth_user2['auth_user_id'],auth_user3['auth_user_id']])
    assert (dm['dm_name'] == "tomh0, tomh1, tomh2")  
      
