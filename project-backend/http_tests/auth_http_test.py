import requests
from src import config
BASE_URL =  config.url

'''
auth_login server testing functions
'''

'''
test 1: Email entered is not registered
'''

def test_login_email_not_registered(): 
    
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login/v2", json={
        'email': 'no@gmail.com',
        'password': 'z5270707',
    })
    assert login_resp.status_code == 400


'''
test 2: Password is not correct
'''

def test_login_password_incorrect():
    
    requests.delete(f"{BASE_URL}/clear/v1")
    # register in server
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login/v2", json={
        'email': 'z5270707@gmail.com',
        'password': '666666',
    })
    assert login_resp.status_code == 400



def test_login_success():
    '''
    test if login works on server
    
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload = register_resp.json()

    #test logout in server
    logout_resp = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    payload2 = logout_resp.json()

    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
    })
    payload3 = login_resp.json()

    assert payload['auth_user_id'] == payload3['auth_user_id']
    assert payload2['is_success'] == True
    assert login_resp.status_code == 200



'''
auth_logout server testing functions
'''

def test_logout_success():
    '''
    successfully logout server
    '''
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload = register_resp.json()

    #test logout in server
    logout_resp = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    payload2 = logout_resp.json()

    assert payload2['is_success'] == True
    assert logout_resp.status_code == 200

def test_logout_token_invalid():
    '''
    successfully logout server
    '''
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload = register_resp.json()

    #test logout in server
    logout_resp = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token'] + "abc"})
    
    assert logout_resp.status_code == 403

def test_logout_not_success():
    '''
    unsuccessful logout server
    '''
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload = register_resp.json()

    #test logout in server
    logout_resp = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    payload2 = logout_resp.json()

    assert payload2['is_success'] == True
    assert logout_resp.status_code == 200
    
    #logout again
    logout_resp2 = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    
    assert logout_resp2.status_code == 403


'''
auth_register server testing functions
'''
'''
test 1: Email entered is not a valid email
'''
def test_register_email_invalid():
    
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid email in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    assert register_resp.status_code == 400


'''
test 2: Email address is already being used by another user
'''
def test_register_email_used():
    
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register email in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hebe@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    assert register_resp.status_code == 200

    # register used email in server
    register_resp_2 = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hebe@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    assert register_resp_2.status_code == 400


    

'''
test 3: Password entered is less than 6 characters long 
'''
def test_register_password_less_than_six():
    
   
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid password in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hello@gmail.com',
        'password': '0',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    assert register_resp.status_code == 400


    
'''
test 4: name_first is less than 1 character in length, that is, empty firstname
'''
def test_register_no_firstname():
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid firstname in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hello@gmail.com',
        'password': 'z5270707',
        'name_first': '',
        'name_last': 'Sun'
    })
    
    assert register_resp.status_code == 400



'''
test 5: name_first is more than 50 characters in length, that is, too long firstname
'''
def test_register_long_firstname():
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid firstname in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hello@gmail.com',
        'password': 'z5270707',
        'name_first': 'hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha',
        'name_last': 'Sun'
    })
    
    assert register_resp.status_code == 400

        
'''
test 6: name_last is less than 1 character in length, that is, empty lastname
'''
def test_register_no_lastname():
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid lastname in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hello@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': ''
    })
    
    assert register_resp.status_code == 400




'''
test 7: name_first is more than 50 characters in length, that is, too long firstname
'''
def test_register_long_lastname():
    
    requests.delete(f"{BASE_URL}/clear/v1")
    
    # register invalid firstname in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'hello@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha',
    })
    
    assert register_resp.status_code == 400


'''
test 8: user register successful
'''        
def test_register_success():
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #register in server
    register_resp = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    payload = register_resp.json()

    #test logout in server
    logout_resp = requests.post(f"{BASE_URL}/auth/logout/v1", json= {'token': payload['token']})
    payload2 = logout_resp.json()

    #test login in server
    login_resp = requests.post(f"{BASE_URL}/auth/login/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
    })
    payload3 = login_resp.json()

    assert payload['auth_user_id'] == payload3['auth_user_id']
    assert payload2['is_success'] == True
    assert login_resp.status_code == 200

'''
tests for restore passwords
'''
def test_reset_request_not_regestered():
    '''
    reset when not registered
    '''
    
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #request reset
    reset_request_resp = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json={
            'email': 'z5270707@gmail.com'
            })
    assert reset_request_resp.status_code == 400

def test_reset_request_success():
    '''
    request working
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #register in server
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    #request reset
    reset_request_resp = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json={
            'email': 'z5270707@gmail.com'
            })
    assert reset_request_resp.status_code == 200

def test_invalid_reset():
    '''
    reset code invalid
    '''
    #Resets the internal data of the application to it's initial state
    requests.delete(f"{BASE_URL}/clear/v1")
    
    #register in server
    requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z5270707@gmail.com',
        'password': 'z5270707',
        'name_first': 'Sunny',
        'name_last': 'Sun'
    })
    
    #request reset
    reset_request_resp = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json={
            'email': 'z5270707@gmail.com'
            })
    
    assert reset_request_resp.status_code == 200
    
    reset_resp = requests.post(f"{BASE_URL}/auth/passwordreset/reset/v1", json={
            'reset_code': 'nomatter', 
            'new_password': '1234567', 
            })
    
    assert reset_resp.status_code == 400