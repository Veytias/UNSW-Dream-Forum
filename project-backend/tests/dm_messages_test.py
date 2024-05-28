import pytest
from src.auth import auth_register_v2
from src.dm import dm_messages_v1, dm_create_v1
from src.message import message_senddm_v1
from src.other import clear_v1
from src.helper import load_data, save_data
import src.error


def test_dm_id_invalid():
    clear_v1()
    user = auth_register_v2("dmidinvalid@gmail.com","a123456789","Micky","Mouse")
    with pytest.raises(src.error.InputError):
        dm_messages_v1(user['token'],10,0)

def test_dm_start_error():
    clear_v1()
    user1 = auth_register_v2("dmstarterror1@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("dmstarterror2@gmail.com","a123456789","Micky","Mouse")
    dm = dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    with pytest.raises(src.error.InputError):
        dm_messages_v1(user1['token'],dm['dm_id'],50)

def test_user_not_in_dm():
    clear_v1()
    user1 = auth_register_v2("notindm1@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("notindm2@gmail.com","a123456789","Micky","Mouse2")
    user3 = auth_register_v2("notindm3@gmail.com","a123456789","Micky","Mouse3")
    dm = dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    with pytest.raises(src.error.AccessError):
        dm_messages_v1(user3['token'],dm['dm_id'],0)

def test_dm_single_message_success():
    clear_v1()  
    user1 = auth_register_v2("notinchannel@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    dm = dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    message_senddm_v1(user1['token'],dm['dm_id'],'Hello World')
    messages = dm_messages_v1(user1['token'],dm['dm_id'],0)

    assert len(messages['messages']) == 1
def test_dm_multiple_messages_success():
    clear_v1()
    user1 = auth_register_v2("notinchannel@gmail.com","a123456789","Micky","Mouse")
    user2 = auth_register_v2("notinchannel2@gmail.com","a123456789","Micky","Mouse2")
    dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    dm = dm_create_v1(user1['token'],[user1['auth_user_id'],user2['auth_user_id']])
    message_senddm_v1(user1['token'],dm['dm_id'],'Hello World')
    message_senddm_v1(user1['token'],dm['dm_id'],'Hello World')
    message_senddm_v1(user1['token'],dm['dm_id'],'Hello World')
   
    messages = dm_messages_v1(user1['token'],dm['dm_id'],0)
    assert len(messages['messages']) == 3
     
