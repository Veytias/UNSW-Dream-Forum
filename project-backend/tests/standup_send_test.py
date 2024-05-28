import pytest
from src.auth import auth_register_v2 as register
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
from src.standup import standup_send, standup_start
from src.channel import channel_invite_v2
from src.dm import dm_messages_v1, dm_create_v1
from src.message import message_senddm_v1
import src.error

'''
InputError Case
Channel ID is not a valid channel
'''

def test_invalid_channel():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    channels_create_v2(user_1['token'], 'channel_1', True)
    with pytest.raises(src.error.InputError):
        # assume that channel_id 2 has not been created before
        standup_send(user_1['token'], 2, 'Hi')

'''
Message is more than 1000 characters
'''

def test_too_long_message():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    with pytest.raises(src.error.InputError):
        standup_send(user_1['token'], cha_1['channel_id'], 'A' * 1001)

'''
An active standup is not currently running in this channel
'''
def test_standup_is_not_running():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    with pytest.raises(src.error.InputError):
        standup_send(user_1['token'], cha_1['channel_id'], 'Hello')

'''
AccessError Case
The authorised user is not a member of the channel that the message is within
'''
def test_authorised_user():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","654321", "Khahood", "Table")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    standup_start(user_1['token'], cha_1['channel_id'], 1)
    with pytest.raises(src.error.AccessError):
        standup_send(user_2['token'], cha_1['channel_id'], 'Hello')

'''
Success Case
'''
def test_success_send():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register("user_2@gmail.com","654321", "Khahood", "Table")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    cha_2 = channels_create_v2(user_2['token'], 'channel_2', True)
    dm_create_v1(user_1['token'],[user_1['auth_user_id'],user_2['auth_user_id']])
    dm = dm_create_v1(user_1['token'],[user_1['auth_user_id'],user_2['auth_user_id']])
    message_senddm_v1(user_1['token'],dm['dm_id'],'Hello World')
    dm_messages_v1(user_1['token'],dm['dm_id'],0)
    channel_invite_v2(user_1['token'], cha_1['channel_id'], user_2['auth_user_id'])
    standup_start(user_1['token'], cha_1['channel_id'], 1)
    standup_send(user_1['token'], cha_1['channel_id'], 'Hello')
    standup_send(user_2['token'], cha_1['channel_id'], 'Hi there')
    standup_start(user_2['token'], cha_2['channel_id'], 1)
    standup_send(user_2['token'], cha_2['channel_id'], 'Also one here')

    data = load_data()

    for stdup in data['standups']:
        if stdup['standup_id'] == 1 and stdup['channel_id'] == cha_1['channel_id']:
            res = stdup['messages']
        if (stdup['standup_id'] == 2 and stdup['channel_id'] == cha_2['channel_id']):
            res2 = stdup['messages']
    
    expect_msg = [{'name_first': 'Jimmy', 'message' : 'Hello', 'u_id' : user_1['auth_user_id']},
                  {'name_first': 'Khahood', 'message' : 'Hi there', 'u_id' : user_2['auth_user_id']}]

    expect_msg2 = [{'name_first': 'Khahood', 'message' : 'Also one here', 'u_id' : user_2['auth_user_id']}]

    assert res == expect_msg
    assert res2 == expect_msg2
