import pytest
from src.message import message_send_v2 as m_send
from src.message import message_senddm_v1 as m_senddm
from src.other import search_v2 as search
from src.channels import channels_create_v2 as channels_create
from src.dm import dm_create_v1 as dm_create
from src.auth import auth_register_v2 as register
#from src.helper import load_data
from src.other import clear_v1 as clear
import src.error

'''
Inputerror, query_str is above 1000 characters
'''
def test_message_too_long():
    '''
    Length of message is over 1000 characters, raise InputError
    '''
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    message = "hi"*666
    
    with pytest.raises(src.error.InputError):
        search(token1, message)

'''
Accesserror, token invalid
'''           
def test_token_invalid():
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']
    message = "hi"

    with pytest.raises(src.error.AccessError):
        search(token1 + 'abc', message)

def test_search_empty_str():
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')

    token1 = user1['token']
    channel_one = channels_create(token1, 'name', True)
    channel_one['channel_id']

    m_send(token1, 1, "mochi")
    m_send(token1, 1, "chocolate mochi")

    message = search(token1, "")

    assert message['messages'] == []


def test_search_success_ch():
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')

    token1 = user1['token']
    
    channels_create(token1, 'name', True)
    channels_create(token1, 'name2', True)

    m_send(token1, 1, "mochi")
    m_send(token1, 1, "chocolate mochi")

    message = search(token1, "mochi")
    assert len(message['messages']) == 2

    message = search(token1, "ksn")
    assert len(message['messages']) == 0

def test_search_success_dm():
    clear()
    user1 = register('validemail1@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('secondemail@gmail.com', '54321Hello', 'Mikey', 'Mouse')

    token1 = user1['token']
    dm_create(token1, [user2['auth_user_id']])

    m_senddm(token1, 1, "mochi")
    m_senddm(token1, 1, "chocolate mochi")

    message = search(token1, "mochi")
    assert len(message['messages']) == 2

    message = search(token1, "ksn")
    assert len(message['messages']) == 0


