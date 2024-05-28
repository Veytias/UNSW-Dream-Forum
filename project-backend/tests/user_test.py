import pytest
from src.auth import auth_register_v2 as register
from src.auth import auth_logout_v1 as logout
import src.user as user
import src.error as error
#from src.helper import load_data
from src.other import clear_v1 as clear
from src.message import getUserId
import src.config as config

PORT = config.port
'''
tests for user_profile function
'''


def test_userprofile_invalid_uid():
    '''
    u_id is invalid
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_v2(token1, -2)
    
    
def test_userprofile_invalid_token():
    '''
    token is invalid
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.AccessError):
        user.user_profile_v2(token1 + "abx", 1)

def test_userprofile_invalid_token_logged_out():
    '''
    token is invalid
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']
    
    logout(token1)

    with pytest.raises(error.AccessError):
        user.user_profile_v2(token1, 1)
        
def test_userprofile_invalid_token_empty():
    '''
    token is invalid
    '''
    clear()
    register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
  
    with pytest.raises(error.AccessError):
        user.user_profile_v2("", 1)

def test_userprofile_success():
    '''
    user_profile working properly
    '''
    clear()
    
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    u_id1 = getUserId(token1)
   
    user_profile1 = user.user_profile_v2(token1, u_id1)

    assert user_profile1 == {
        'user': {
            'u_id': u_id1,
            'email': 'validemai@gmail.com',
            'name_first': 'Hayden',
            'name_last': 'Everest',
            'handle_str': 'haydeneverest',
            'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }
    }

    assert user_profile1['user']['email'] == 'validemai@gmail.com'
    assert user_profile1['user']['name_first'] == 'Hayden'
    
'''
tests for user_setname function
'''

def test_setname_firstname_wrong_format():
    '''
    first name too long or too short
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_setname_v2(token1, 'aha'*100, 'Everest')
    
    with pytest.raises(error.InputError):
        user.user_profile_setname_v2(token1, '', 'Everest')


def test_setname_lastname_wrong_format():
    '''
    last name too long or too short
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_setname_v2(token1, 'Joanna', 'aha'*50)
    
    with pytest.raises(error.InputError):
        user.user_profile_setname_v2(token1, 'Joanna', '')


def test_setname_invalid_token():
    
    '''
    token invalid
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.AccessError):
        user.user_profile_setname_v2(token1 + "abc", 'Joanna', 'Jones')

def test_setname_success():
    '''
    setname working properly
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']
    u_id1 = getUserId(token1)
    user_setname = user.user_profile_setname_v2(token1, 'Jo', 'Snow')

    assert user_setname == {}
    
    user_profile_after_setname = user.user_profile_v2(token1, u_id1)

    assert user_profile_after_setname['user']['name_first'] == 'Jo'
    assert user_profile_after_setname['user']['name_last'] == 'Snow'


'''
tests for user_profile_setemail
'''

def test_setemail_invalid_email_format():
    '''
    email wrong format
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_setemail_v2(token1, 'invalid.mail')
    with pytest.raises(error.InputError):
        user.user_profile_setemail_v2(token1, '@mail.com')
    with pytest.raises(error.InputError):
        user.user_profile_setemail_v2(token1, '123@mail.')

def test_setemail_email_taken():
    '''
    email has been registered
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']
    register('email@gmail.com', '123abcd', 'firstname', 'lastname')

    with pytest.raises(error.InputError):
        user.user_profile_setemail_v2(token1, 'email@gmail.com')


def test_setemail_invalid_token():
    '''
    the token is invalid
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    with pytest.raises(error.AccessError):
        user.user_profile_setemail_v2(token1 + 'abc', 'Joanna@gmail.com')


def test_setemail_success():
    '''
    setemail working properly
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    set_email1 = user.user_profile_setemail_v2(token1, "Joanna@gmail.com")

    assert set_email1 == {}

    u_id1 = getUserId(token1)
    user_profile1 = user.user_profile_v2(token1, u_id1)
    
    new_email = user_profile1['user']['email']

    assert new_email == "Joanna@gmail.com"


'''
tests for set_handle function
'''
def test_sethandle_handle_taken():
    '''
    handle has been taken
    '''
    clear()
    register("testhandle3@gmail.com", "123456", "John", "Smith")

    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token2 = user2['token']
    
    with pytest.raises(error.InputError):
        user.user_profile_sethandle_v1(token2,'johnsmith')


def test_sethandle_token_invalid():
    '''
    token invalid
    '''
    clear()
    register("testhandle3@gmail.com", "123456", "John", "Smith")


    user2 = register('email@gmail.com', '123abcd', 'firstname', 'lastname')
    token2 = user2['token']
    
    with pytest.raises(error.AccessError):
        user.user_profile_sethandle_v1(token2 + 'abc','judyjune')

def test_handle_less_than_3():
    '''
    handle wrong format: short
    '''
    clear()
    user1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_sethandle_v1(token1,'ju')


def test_handle_more_than_20():
    '''
    handle wrong format: long
    '''
    clear()
    user1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    token1 = user1['token']

    with pytest.raises(error.InputError):
        user.user_profile_sethandle_v1(token1,'ju'*20)


def test_sethandle_success():
    '''
    sethandle working properly
    '''
    clear()
    user1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    token1 = user1['token']
    u_id1 = user1['auth_user_id']

    user.user_profile_sethandle_v1(token1,'juju')

    user_profile1 = user.user_profile_v2(token1, u_id1)

    assert user_profile1 == {
        'user': {
            'u_id': u_id1,
            'email': "testhandle3@gmail.com",
            'name_first': "John",
            'name_last': 'Smith',
            'handle_str': 'juju',
            'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        },
    }

    
'''
tests for users_all function
'''

def test_users_all_token_invalid():
    '''
    token invalid
    '''
    clear()
    user1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    token1 = user1['token']

    with pytest.raises(error.AccessError):
        user.users_all_v1(token1 + 'abc')


def test_users_all_success_one_user():
    '''
    users_all working properly for one user
    '''
    clear()
    user1 = register('validemai@gmail.com', '123abcde', 'Hayden', 'Everest')
    token1 = user1['token']

    users = user.users_all_v1(token1)

    assert users == {'users' : 
        [{
        'u_id': user1['auth_user_id'],
        'email': 'validemai@gmail.com',
        'name_first': 'Hayden',
        'name_last': 'Everest',
        'handle_str': 'haydeneverest',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }]
    }


def test_users_all_success_two_user():
    '''
    users_all working properly for two user
    '''
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')

    user2 = register('myschool@gmail.com', '123abcd', 'firstname', 'lastname')
    token2 = user2['token']

    all_users = user.users_all_v1(token2)

    
    assert all_users == {'users' : 
        [{
        'u_id': user1['auth_user_id'],
        'email': 'bye@gmail.com',
        'name_first': 'Hayden',
        'name_last': 'Everest',
        'handle_str': 'haydeneverest',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }, {
        'u_id': user2['auth_user_id'],
        'email': 'myschool@gmail.com',
        'name_first': 'firstname',
        'name_last': 'lastname',
        'handle_str': 'firstnamelastname',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }]
    }

'''
test upload photo
'''
def test_uploadphoto_invalid_token():
    clear()
    user1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    token1 = user1['token']
    image_url = "https://static0.thethingsimages.com/wordpress/wp-content/uploads/2018/08/Kittens-via-WallpaperSite.jpg"
    
    with pytest.raises(error.AccessError):
        user.user_profile_uploadphoto_v1(token1 + 'abc', image_url, 0, 0, 200, 200)

def test_uploadphoto_url_invalid():
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    url = "www.radioreference.com/apps/audio/?ctid=5586"
    with pytest.raises(error.InputError):
        user.user_profile_uploadphoto_v1(token1, url, 0, 0, 200, 200)

def test_uploadphoto_url_invalid2():
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    image_url = "https://static0.thethingsimages.com/wordpress/wp-content/uploads/2018/08/Kittens-via-WallpaperSite.jpg"
    with pytest.raises(error.InputError):
        user.user_profile_uploadphoto_v1(token1,image_url, 0, 0, 200, 200)

def test_uploadphoto_not_jpg():
    
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    image_url = "https://www.copytrans.net/app/uploads/sites/3/2014/06/cta-ipad-apps-appear.png"
    
    with pytest.raises(error.InputError):
        user.user_profile_uploadphoto_v1(token1, image_url, 0, 0, 200, 200)

def test_uploadphoto_crop_exceed_bound1():
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    image_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    with pytest.raises(error.InputError):
        user.user_profile_uploadphoto_v1(token1, image_url, -100, -100, 200, 200)


def test_uploadphoto_crop_exceed_bound2():
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    image_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    with pytest.raises(error.InputError):
        user.user_profile_uploadphoto_v1(token1, image_url, 0, 0, 20000, 200)    
    
def test_uploadphoto_success():
    clear()
    user1 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token1 = user1['token']
    image_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    assert user.user_profile_uploadphoto_v1(token1, image_url, 0, 0, 1000, 1000) == {}    

def test_uploadphoto_success_default_image():
    
    clear()
    register('hello@gmail.com', '123abcde', 'Hayden', 'Everest')
    user2 = register('bye@gmail.com', '123abcde', 'Hayden', 'Everest')
    
    token2 = user2['token']
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Dog_head%2C_Alaska_02.jpg/1200px-Dog_head%2C_Alaska_02.jpg"
    
    assert user.user_profile_uploadphoto_v1(token2, image_url, 0, 0, 800, 800) == {}