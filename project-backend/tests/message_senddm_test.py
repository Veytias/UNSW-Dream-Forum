import pytest
from src.message import message_senddm_v1
from src.dm import dm_create_v1 as dm_create
from src.auth import auth_register_v2 as register
from src.helper import load_data
from src.other import clear_v1 as clear
import src.error


'''
tests for message send functions
'''

def test_message_too_long():
    '''
    Length of message is over 1000 characters, raise InputError
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '123asdbc', 'Mickey', 'Mouse')
    
    token1 = user1['token']
    u_id2 = user2['auth_user_id']
    dm = dm_create(token1, [u_id2])
    dm_one_id = dm['dm_id']
    message_content = "hi"*666
    
    with pytest.raises(src.error.InputError):
        message_senddm_v1(token1, dm_one_id, message_content)

def test_dm_id_None():
    '''
    success message send test case
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']
    
    message_content = "hi"

    with pytest.raises(src.error.InputError):
        message_senddm_v1(token1, None, message_content)
       

def test_invalid_token():
    '''
    Token invalid, raise AccessError
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '123asdbc', 'Mickey', 'Mouse')
    
    token1 = user1['token']
    u_id2 = user2['auth_user_id']
    dm = dm_create(token1, [u_id2])
    dm_one_id = dm['dm_id']
    message_content = "hi"
    
    with pytest.raises(src.error.AccessError):
        message_senddm_v1(token1 + "abc", dm_one_id, message_content)
        
       
        

def test_user_not_joined():
    '''
    the user is not joined in the dm, raise AccessError
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '123asdbc', 'Mickey', 'Mouse')
    user3 = register('validemail3@gmail.com', 'password', 'Larry', 'Sherbert')
    
    token1 = user1['token']
    u_id2 = user2['auth_user_id']
    token3 = user3['token']
    dm = dm_create(token1, [u_id2])
    dm_one_id = dm['dm_id']
    
    message_content = "hi"
    
    with pytest.raises(src.error.AccessError):
        message_senddm_v1(token3, dm_one_id, message_content)
        
       

def test_message_send_success():
    '''
    success message send test case
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('validemail2@gmail.com', '123asdbc', 'Mickey', 'Mouse')
    user3 = register('validemail3@gmail.com', 'password', 'Larry', 'Sherbert')
    
    token1 = user1['token']
    token3 = user3['token']
    u_id2 = user2['auth_user_id']
    u_id1 = user1['auth_user_id']
    dm0 = dm_create(token1, [u_id2])
    dm = dm_create(token3, [u_id1])
    dm_one_id = dm['dm_id']
    
    message_content = "hi"
    message_senddm_v1(token1, dm0['dm_id'], message_content)
    message_id1 = message_senddm_v1(token1, dm_one_id, message_content)
    
    assert message_id1['message_id'] == 2
        
       
