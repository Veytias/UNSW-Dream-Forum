import pytest
from src.auth import auth_register_v2 as register
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
from src.standup import standup_start
import src.error
import time
from datetime import datetime,timedelta

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
        standup_start(user_1['token'], 2, 1)

'''
Standup is currently active in channel
'''

def test_currently_active():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    standup_start(user_1['token'], cha_1['channel_id'], 1)
    with pytest.raises(src.error.InputError):
        standup_start(user_1['token'], cha_1['channel_id'], 1)

'''
AccessError case
test 1 Authorised user is not a member of channel with channel_id.
'''
def test_authorised_user():

	clear_v1()

	user_1 = register('user_1@gmail.com', '123456', 'first_user_1', 'last_user_1')
	user_2 = register('user_2@gmail.com', '678901', 'first_user_2', 'last_user_2')
	cha_id = channels_create_v2(user_1['token'], 'new_channel', True)
	channels_create_v2(user_1['token'], 'channel2', True)
	# user_2 try to accese channel 1 details which is prohibit
	with pytest.raises(src.error.AccessError):
            standup_start(user_2['token'], cha_id['channel_id'], 1)

'''
Success case
'''
def test_success():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    user_2 = register('user_2@gmail.com', '678901', 'first_user_2', 'last_user_2')
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    cha_2 = channels_create_v2(user_2['token'], 'new_channel2', True)
    output = standup_start(user_1['token'], cha_1['channel_id'], 1)
    
    now = datetime.now()
    finish_time = (now + timedelta(seconds=1)).timestamp()

    assert abs(output['time_finish'] - int(finish_time)) == 0

    output = standup_start(user_2['token'], cha_2['channel_id'], 1)

    now = datetime.now()
    finish_time = (now + timedelta(seconds=1)).timestamp()

    assert abs(output['time_finish'] - int(finish_time)) == 0

def test_redo_standup():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    standup_start(user_1['token'], cha_1['channel_id'], 1)