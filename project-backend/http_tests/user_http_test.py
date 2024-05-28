import requests
from src import config
BASE_URL =  config.url
PORT = config.port
'''
server tests for message user profile function
'''

def test_userprofile_invalid_token():
    '''
    token is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']+'abc'}&u_id={payload['auth_user_id']}")


    assert profile_resp.status_code == 403
    
def test_userprofile_invalid_token_logged_out():
    '''
    token is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={payload['auth_user_id']}")


    assert profile_resp.status_code == 403
    
def test_userprofile_invalid_uid():
    '''
    u_id is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={'-7'}")


    assert profile_resp.status_code == 400

def test_userprofile_success():
    '''
    user_profile working properly
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={payload['auth_user_id']}")


    payload2 = profile_resp.json()

    assert profile_resp.status_code == 200
    assert payload2['user']['email'] == 'z5270707@gmail.com'
    assert payload2['user']['name_last'] == 'Sun'

'''
server tests for user_setname function
'''

def test_setname_firstname_wrong_format():
    '''
    first name too long or too short
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setname_resp = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'], 
        'name_first': 'aha'*100,
        'name_last': 'White'
    })

    assert setname_resp.status_code == 400

    setname_resp2 = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'], 
        'name_first': '',
        'name_last': 'White'
    })

    assert setname_resp2.status_code == 400

def test_setname_lastname_wrong_format():
    '''
    last name too long or too short
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setname_resp = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'], 
        'name_first': 'Anna',
        'name_last': 'Why'*100
    })

    assert setname_resp.status_code == 400

    setname_resp2 = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'], 
        'name_first': 'Anna',
        'name_last': ''
    })

    assert setname_resp2.status_code == 400

def test_setname_invalid_token():
    
    '''
    token invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setname_resp = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'] + 'abc', 
        'name_first': 'Anna',
        'name_last': 'White'
    })

    assert setname_resp.status_code == 403

def test_setname_success():
    '''
    setname working properly
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setname_resp = requests.put(f"{BASE_URL}/user/profile/setname/v2", json={
        'token': payload['token'], 
        'name_first': 'Anna',
        'name_last': 'White'
    })

    assert setname_resp.status_code == 200

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={payload['auth_user_id']}")


    payload2 =profile_resp.json()
    assert payload2['user']['name_first'] == "Anna"
    assert payload2['user']['name_last'] == "White"

'''
tests for user_profile_setemail
'''

def test_setemail_invalid_email_format():
    '''
    email wrong format
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setemail_resp = requests.put(f"{BASE_URL}/user/profile/setemail/v2", json={
        'token': payload['token'], 
        'email': 'mail.com'
    })

    assert setemail_resp.status_code == 400

    setemail_resp2 = requests.put(f"{BASE_URL}/user/profile/setemail/v2", json={
        'token': payload['token'], 
        'email': 'wo@email'
    })
    assert setemail_resp2.status_code == 400

def test_setemail_email_taken():
    '''
    email has been registered
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': 'ahh1234',
        'name_first': 'Love',
        'name_last': 'You'
    })
    
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setemail_resp = requests.put(f"{BASE_URL}/user/profile/setemail/v2", json={
        'token': payload['token'], 
        'email': 'goodjob@gmail.com',
    })

    assert setemail_resp.status_code == 400

def test_setemail_invalid_token():
    '''
    the token is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setemail_resp = requests.put(f"{BASE_URL}/user/profile/setemail/v2", json={
        'token': payload['token'] + 'abc', 
        'email': 'hello@gmail.com'
    })

    assert setemail_resp.status_code == 403

def test_setemail_success():
    '''
    setemail working properly
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    setemail_resp = requests.put(f"{BASE_URL}/user/profile/setemail/v2", json={
        'token': payload['token'], 
        'email': 'hello@gmail.com'
    })

    assert setemail_resp.status_code == 200

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={payload['auth_user_id']}")


    payload2 =profile_resp.json()
    assert payload2['user']['email'] == 'hello@gmail.com'

'''
tests for set_handle function
'''
def test_sethandle_handle_taken():
    '''
    handle has been taken
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'testhandle3@gmail.com',
        'password': 'abc123',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    sethandle_resp = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json={
        'token': payload['token'], 
        'handle_str': 'johnsmith'
    })

    assert sethandle_resp.status_code == 400

def test_sethandle_token_invalid():
    '''
    token invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    sethandle_resp = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json={
        'token': payload['token'] + 'abc', 
        'handle_str': 'johnsmith'
    })

    assert sethandle_resp.status_code == 403

def test_handle_less_than_3():
    '''
    handle wrong format: short
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    sethandle_resp = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json={
        'token': payload['token'], 
        'handle_str': 'ju'
    })

    assert sethandle_resp.status_code == 400

def test_handle_more_than_20():
    '''
    handle wrong format: long
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    sethandle_resp = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json={
        'token': payload['token'], 
        'handle_str': 'ju'*20
    })

    assert sethandle_resp.status_code == 400

def test_sethandle_success():
    '''
    sethandle working properly
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    sethandle_resp = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json={
        'token': payload['token'], 
        'handle_str': 'applepen'
    })

    assert sethandle_resp.status_code == 200

    profile_resp = requests.get(f"{BASE_URL}/user/profile/v2?token={payload['token']}&u_id={payload['auth_user_id']}")


    payload2 =profile_resp.json()
    assert payload2['user']['handle_str'] == 'applepen'

'''
tests for users_all function
'''

def test_users_all_token_invalid():
    '''
    token invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    usersall_resp = requests.get(f"{BASE_URL}/users/all/v1", json={
        'token': payload['token'] + 'abc',
    })
    assert usersall_resp.status_code == 403

def test_users_all_success_one_user():
    '''
    users_all working properly for one user
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    usersall_resp = requests.get(f"{BASE_URL}/users/all/v1?token={payload['token']}")
    payload2 = usersall_resp.json()
    assert usersall_resp.status_code == 200
    assert payload2['users'] == [{
        'u_id': payload['auth_user_id'],
        'email': 'z5270707@gmail.com',
        'name_first': 'Sunny',
        'name_last': 'Sun',
        'handle_str': 'sunnysun',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }]

def test_users_all_success_two_user():
    '''
    users_all working properly for two user
    '''
        #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()

    register_resp2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'goodjob@gmail.com',
        'password': 'ahh1234',
        'name_first': 'Lovely',
        'name_last': 'You'
    })
    payload1 = register_resp2.json()

    usersall_resp = requests.get(f"{BASE_URL}/users/all/v1?token={payload['token']}")

    payload2 = usersall_resp.json()

    assert usersall_resp.status_code == 200

    assert payload2['users'] == [{
        'u_id': payload['auth_user_id'],
        'email': 'z5270707@gmail.com',
        'name_first': 'Sunny',
        'name_last': 'Sun',
        'handle_str': 'sunnysun',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }, {
        'u_id': payload1['auth_user_id'],
        'email': 'goodjob@gmail.com',
        'name_first': 'Lovely',
        'name_last': 'You',
        'handle_str': 'lovelyyou',
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        }]
        
'''
user uploadphoto test
'''
def test_upload_photo_invalid_token():
    '''
    when token is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    
    profile_img_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    upload_resp = requests.post(f"{BASE_URL}/user/profile/uploadphoto/v1", json={
        "token": payload['token'] + "abc", 
        "img_url": profile_img_url, 
        "x_start": "0",
        "y_start": "0",
        "x_end": "300",
        "y_end": "300",
    })
    
    assert upload_resp.status_code == 403
    
def test_uploadphoto_url_invalid():
    '''
    test when the url is invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    
    fake_img_url = "https"
    
    upload_resp = requests.post(f"{BASE_URL}/user/profile/uploadphoto/v1", json={
        "token": payload['token'], 
        "img_url": fake_img_url, 
        "x_start": "0",
        "y_start": "0",
        "x_end": "300",
        "y_end": "300",
    })
    
    assert upload_resp.status_code == 400
    
def test_uploadphoto_not_jpg():
    '''
    format not jpg
    '''

    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    
    png_img_url = "https://www.copytrans.net/app/uploads/sites/3/2014/06/cta-ipad-apps-appear.png"
    
    upload_resp = requests.post(f"{BASE_URL}/user/profile/uploadphoto/v1", json={
        "token": payload['token'], 
        "img_url": png_img_url, 
        "x_start": "0",
        "y_start": "0",
        "x_end": "300",
        "y_end": "300",
    })
    
    assert upload_resp.status_code == 400

def test_uploadphoto_crop_exceed_bound():
    '''
    crop values not valid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    
    profile_img_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    upload_resp = requests.post(f"{BASE_URL}/user/profile/uploadphoto/v1", json={
        "token": payload['token'], 
        "img_url": profile_img_url, 
        "x_start": "-100",
        "y_start": "-200",
        "x_end": "300",
        "y_end": "300",
    })
    
    assert upload_resp.status_code == 400

def test_uploadphoto_success():
    '''
    successfully upload
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp= requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })

    payload = register_resp.json()
    
    profile_img_url = "https://www.baldivisvet.com.au/wp-content/uploads/2017/10/hd-cute-cat-wallpaper.jpg"
    
    upload_resp = requests.post(f"{BASE_URL}/user/profile/uploadphoto/v1", json={
        "token": payload['token'], 
        "img_url": profile_img_url, 
        "x_start": "0",
        "y_start": "0",
        "x_end": "1000",
        "y_end": "1000",
    })
    
    assert upload_resp.status_code == 200