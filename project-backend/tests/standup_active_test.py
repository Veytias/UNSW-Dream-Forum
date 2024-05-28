import pytest
from src.auth import auth_register_v2 as register
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
from src.standup import standup_start, standup_active
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
        standup_active(user_1['token'], 2)

'''
Success case
'''
def test_success_active():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    standup_start(user_1['token'], cha_1['channel_id'], 1)
    res = standup_active(user_1['token'], cha_1['channel_id'])
    
    now = datetime.now()
    finish_time = (now + timedelta(seconds=1)).timestamp()

    expect = {'is_active': True, 'time_finish': int(finish_time)}

    assert res == expect


def test_success_not_active_yet():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    res = standup_active(user_1['token'], cha_1['channel_id'],)
    
    expect = {'is_active': False, 'time_finish': None}
    assert res == expect

def test_success_active_finished():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jimmy", "Brother")
    cha_1 = channels_create_v2(user_1['token'], 'channel_1', True)
    standup_start(user_1['token'], cha_1['channel_id'], 1)
    time.sleep(1)
    res = standup_active(user_1['token'], cha_1['channel_id'])

    expect = {'is_active': False, 'time_finish': None}
    assert res == expect
    


