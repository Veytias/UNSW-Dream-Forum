import pytest 
from src.auth import auth_register_v2 as register
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1
import src.user as user
import src.error
from src.other import clear_v1 as clear
from src.user import user_stats_v1, users_stats_v1
from src.helper import load_data, save_data


'''
token invalid
'''
def test_token_invalid():
    clear()
    user1 = register('validemail@gmail.com', '12345Hello', 'Barry', 'Allen')
    token1 = user1['token']

    with pytest.raises(src.error.AccessError):
        user_stats_v1(token1+'abc')

'''
test user_stats_v1 function
'''
def test_user_stats():
    clear()
    user1 = register('validemail@gmail.com', '12345Hello', 'Barry', 'Allen')
    user2 = register('validemail2@gmail.com', '123asdHello', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', '123jsdHello', 'Rick', 'Pickle')
    token1 = user1['token']

    create_ch = channels_create_v2(token1, 'name1', True)
    create_dm = dm_create_v1(token1, [user2['auth_user_id']])

    message_send_v2(token1, create_ch['channel_id'], 'Hello')
    message_send_v2(token1, create_ch['channel_id'], 'sup')
    message_send_v2(token1, create_ch['channel_id'], 'Hi')
    message_senddm_v1(token1, create_dm['dm_id'], 'lol')

    user_stats_v1(token1)
    user_stats_v1(token1)

    create_ch2 = channels_create_v2(token1, 'name2', True)
    create_dm2 = dm_create_v1(token1, [user3['auth_user_id']])

    message_send_v2(token1, create_ch2['channel_id'], 'Hi')
    message_senddm_v1(token1, create_dm2['dm_id'], 'lol')

    stat_info = user_stats_v1(token1)

    data = load_data()

    assert stat_info['user_stats']['channels_joined'] == data['users'][0]['user_stats']['channels_joined']
    assert stat_info['user_stats']['dms_joined'] == data['users'][0]['user_stats']['dms_joined']
    assert stat_info['user_stats']['messages_sent'] == data['users'][0]['user_stats']['messages_sent']
    assert stat_info['user_stats']['involvement_rate'] == 1

'''
test users_stats_v1 function
'''
def test_users_stats():
    clear()
    user1 = register('validemail@gmail.com', '12345Hello', 'Barry', 'Allen')
    user2 = register('validemail2@gmail.com', '123asdHello', 'Jim', 'Apple')
    user3 = register('validemail3@gmail.com', '123jsdHello', 'Rick', 'Pickle')
    token1 = user1['token']

    create_ch = channels_create_v2(token1, 'name1', True)
    create_dm = dm_create_v1(token1, [user2['auth_user_id']])
    message_send_v2(token1, create_ch['channel_id'], 'Hello')
    message_send_v2(token1, create_ch['channel_id'], 'sup')
    message_send_v2(token1, create_ch['channel_id'], 'Hi')
    message_senddm_v1(token1, create_dm['dm_id'], 'lol')

    users_stats_v1(token1)
    users_stats_v1(token1)

    create_ch2 = channels_create_v2(token1, 'name2', True)
    dm_create_v1(token1, [user3['auth_user_id']])

    message_send_v2(token1, create_ch2['channel_id'], 'Hi')

    stat_info = users_stats_v1(token1)

    data = load_data()

    assert stat_info['dreams_stats']['channels_exist'] == data['dreams_stats']['channels_exist']
    assert stat_info['dreams_stats']['dms_exist'] == data['dreams_stats']['dms_exist']
    assert stat_info['dreams_stats']['messages_exist'] == data['dreams_stats']['messages_exist']
    assert stat_info['dreams_stats']['utilization_rate'] == 1

def test_token_invalid_users():
    clear()
    user1 = register('validemail@gmail.com', '12345Hello', 'Barry', 'Allen')
    token1 = user1['token']

    with pytest.raises(src.error.AccessError):
        users_stats_v1(token1+'abc')



    

   

    




