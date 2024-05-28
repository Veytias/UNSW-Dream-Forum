import pytest
import src.channel
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import load_data
import src.error

#channels_create_v1(auth_user_id, name, is_public)
def test_token_invalid():
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token'] 
    with pytest.raises(src.error.AccessError):
        channels_create_v2(token1+'abc', 'channel_one', True)
def test_channel_name_too_long():
    clear_v1()
    auth_user1 = auth_register_v2('testchannelprivate1@gmail.com','a123456789','tom','h0')
    with pytest.raises(src.error.InputError):
        channels_create_v2(auth_user1['token'],'abcdefghijklmnopqrstuvwxyz',True)

def test_channel_create_success():
    clear_v1()
    auth_user1 = auth_register_v2('testchannelprivate1@gmail.com','a123456789','tom','h0')
    channel_id = channels_create_v2(auth_user1['token'],'name',True)
    create_success = False
    data = load_data()
    for channel in data['channels']:
        if channel_id['channel_id'] == channel['channel_id']:
            create_success = True
    assert create_success == True

def test_channel_create_information():
    clear_v1()
    user1 = auth_register_v2('testmessage@gmail.com','a123456789','tom','h')
    channel_id = channels_create_v2(user1['token'],'name',False)
    data = load_data()
    assert (data['channels'][channel_id['channel_id']-1]['name'] == 'name' and data['channels'][channel_id['channel_id']-1]['is_public'] == False)
     
