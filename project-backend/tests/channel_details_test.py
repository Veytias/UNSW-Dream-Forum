import pytest
from src.auth import auth_register_v2 as register
from src.channel import channel_details_v2 as details
from src.channel import channel_join_v2 as join
from src.channels import channels_create_v2 as create_channel
from src.helper import getUserId, check_token_valid, load_data
from src.other import clear_v1
import src.error
import src.config as config

PORT = config.port

'''
InputError case
test 1 Channel ID is not a valid channel.
'''
def test_channel_invalid():

	clear_v1()

	user_test_1 = register('user_1@gmail.com', '123456', 'first_user_1', 'last_user_1')

	create_channel(user_test_1['token'], 'new_channel', True)
    # access channel_ed 1 which doesn't exist
	with pytest.raises(src.error.InputError):
        	details(user_test_1['token'], 2)
                            
'''
AccessError case
test 1 Authorised user is not a member of channel with channel_id.
'''
def test_authorised_user():

	clear_v1()

	user_test_1 = register('user_1@gmail.com', '123456', 'first_user_1', 'last_user_1')
	user_test_2 = register('user_2@gmail.com', '678901', 'first_user_2', 'last_user_2')
	cha_id = create_channel(user_test_1['token'], 'new_channel', True)
	create_channel(user_test_1['token'], 'channel2', True)
	# user_2 try to accese channel 1 details which is prohibit
	with pytest.raises(src.error.AccessError):
        	details(user_test_2['token'], cha_id['channel_id'])  		

'''
Compare the return data compare to expected data
'''  	
def test_succesful_details():
    clear_v1()
    user_test_1 = register('user_1@gmail.com', '123456', 'Sam', 'Smith')
    user_test_2 = register('user_2@gmail.com', '678901', 'Bird', 'Nest')
    cha_id = create_channel(user_test_1['token'], 'new_channel', True)
    join(user_test_2['token'],cha_id['channel_id'])
    detail = details(user_test_1['token'], cha_id['channel_id'])
    assert detail['name'] == 'new_channel'
    assert detail['is_public'] == True
    assert detail['all_members'] == [{'u_id': user_test_1['auth_user_id'], 'name_first': 'Sam', 'name_last': 'Smith', 'email' : 'user_1@gmail.com','handle_str': 'samsmith', 'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg"},{'u_id': user_test_2['auth_user_id'], 'name_first': 'Bird', 'name_last': 'Nest', 'email' : 'user_2@gmail.com','handle_str': 'birdnest', 'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg"}]
    assert detail['owner_members'] == [{'u_id': user_test_1['auth_user_id'], 'name_first': 'Sam', 'name_last': 'Smith', 'email' : 'user_1@gmail.com','handle_str': 'samsmith', 'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg"},{'email': 'user_2@gmail.com','handle_str': 'birdnest','name_first': 'Bird','name_last': 'Nest','profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",'u_id': 2},
]
	
