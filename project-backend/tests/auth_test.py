import pytest
from src.auth import auth_login_v2 as login
from src.auth import auth_register_v2 as register
from src.auth import auth_logout_v1 as logout
from src.auth import auth_passwordreset_request_v1 as request_reset
from src.auth import auth_passwordreset_reset_v1 as reset_password
import src.error
from src.helper import load_data
from src.other import clear_v1 as clear


'''
auth_login feature testing functions
'''

'''
test 1: Email entered is not a valid email
'''
        
def test_login_email_not_valid():
    
    clear()
    with pytest.raises(src.error.InputError):
        
        login("This_email_is_not_valid", "password")
        
    

'''
test 2: Email entered does not belong to a user
'''

def test_login_email_unregistered():
    
    clear()
    register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(src.error.InputError):
        
        login("notregistered@gmail.com", "password")    


'''
test 3: Password is not correct
'''

def test_login_password_incorrect():
    
    clear()
    register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
    with pytest.raises(src.error.InputError):
        
        login("validemail@gmail.com", "incorrectpassword")

'''
test 4: Login is successful
'''        
        

def test_login_success():
    
    clear()

    data = load_data()
    curr_user_1 = register('test1validemail@gmail.com', 'password', 'Yo','Ho')
    curr_user_2 = login('test1validemail@gmail.com', 'password')
    
    assert (curr_user_1['auth_user_id'] == curr_user_2['auth_user_id'])
    
    for user in data['users']:
        if user['u_id'] == curr_user_2['auth_user_id']:
            assert (user['name_first'] == 'Yo')
    
'''
auth_logout testing
'''
def test_logout_success():
    #logout success
    
    clear()
    curr_user_1 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    login('imsocool@gmail.com', 'password')
    
    assert logout(curr_user_1['token']) == {'is_success': True}


def test_logout_success2():
    #logout success
    
    clear()
    curr_user_1 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    assert logout(curr_user_1['token']) == {'is_success': True}


def test_logout_multiple():
    #multiple logout
    clear()
    curr_user_1 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    curr_user_sessoion2 = login('imsocool@gmail.com', 'password')
    
    assert logout(curr_user_1['token']) == {'is_success': True}
    assert logout(curr_user_sessoion2['token']) == {'is_success': True}

def test_logout_token_invalid():
    clear()
    
    curr_user_1 = register('imsocool@gmail.com', 'password', 'Yo','Ho')
    login('imsocool@gmail.com', 'password')
    with pytest.raises(src.error.AccessError):  
        logout(curr_user_1['token'] + "abc")
    


'''
auth_register feature testing functions
''' 


'''
test 1: Email entered is not a valid email
'''
def test_register_email_invalid():
     
    clear()
    
    with pytest.raises(src.error.InputError):       
        register("invalidgmail.com", "password", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("gmail.com", "password", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("@gmail.com", "password", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("invalid@gmail", "password", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("invalid@gmailcom", "password", "firstname", "lastname")



'''
test 2: Email address is already being used by another user
'''
def test_register_email_used():
    
    clear()
    register("taken@gmail.com", "password", "Hey", "Black") 
    with pytest.raises(src.error.InputError):       
        register("taken@gmail.com", "password2", "Hello", "White")

'''
test 3: Password entered is less than 6 characters long 
'''
def test_register_password_less_than_six():
    
    clear()

    with pytest.raises(src.error.InputError):       
        register("test3@gmail.com", "123", "firstname", "lastname") 
    with pytest.raises(src.error.InputError):       
        register("test3@gmail.com", "", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("test3@gmail.com", " ", "firstname", "lastname")
    with pytest.raises(src.error.InputError):       
        register("test3@gmail.com", "abcde", "firstname", "lastname")


'''
test 4: name_first is less than 1 character in length, that is, empty firstname
'''
def test_register_no_firstname():
    
    clear()
    
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "", "lastname")


'''
test 5: name_first is more than 50 characters in length, that is, too long firstname
'''
def test_register_long_firstname():
    
    clear()
    
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "hhhhhhhhhhhhhhheeeeeeeeeeeeeelllllllllllllllllllllllooooooooooooo", "lastname")
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "123456789012345678901234567890123456789012345678901", "lastname")


        
'''
test 6: name_last is less than 1 character in length, that is, empty lastname
'''
def test_register_no_lastname():
    
    clear()
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "firstname", "")


'''
test 7: name_first is more than 50 characters in length, that is, too long firstname
'''
def test_register_long_lastname():

    clear()
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "firstname", "hhhhhhhhhhhhhhheeeeeeeeeeeeeelllllllllllllllllllllllooooooooooooo")
    with pytest.raises(src.error.InputError):       
        register("test4@gmail.com", "password", "firstname", "123456789012345678901234567890123456789012345678901")  


'''
test 8: user register successful
'''        
def test_register_success():
    
    clear()    
    auth_user_1 = register("testsuccess@gmail.com", "12345678", "You", "success")
    auth_user_2 = login("testsuccess@gmail.com", "12345678")
    
    assert(auth_user_1['auth_user_id'] == auth_user_2['auth_user_id'])          

'''
test 9: check if handle is less than 20 characters, lower case with no " " or "@"
'''

def test_register_handle_format():
    
    clear()    
    data = load_data()
    curr_user = register("testhandle@gmail.com", "123456", "Josephine", "Wiliwilowa Wu")
    
    for user in data['users']:
        if user['u_id'] == curr_user['auth_user_id']:
            assert (user['handle_str'] == 'josephinewiliwilowaw')
    
    curr_user2 = register("testhandle2@gmail.com", "123456", "Ju de", "Idnwbut@in lastname")
    
    for user in data['users']:
        if user['u_id'] == curr_user2['auth_user_id']:
            assert (user['handle_str'] == 'judeidnwbutinlastnam')    


'''
test 10: check if handle is already takne by other user, whether a uew handle could be generated correctly
'''

def test_register_handle_taken():

    clear()    
    data = load_data()
    curr_user_id1 = register("testhandle3@gmail.com", "123456", "John", "Smith")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id1['auth_user_id']:
            assert (user['handle_str'] == 'johnsmith')
            
    curr_user_id2 = register("testhandle4@gmail.com", "987654", "John", "Smith")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id2['auth_user_id']:
            assert (user['handle_str'] == 'johnsmith0')

    curr_user_id3 = register("testhandle5@gmail.com", "woabcd11", "John", "Smith")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id3['auth_user_id']:
            assert (user['handle_str'] == 'johnsmith1')
    
'''
test 11: check if handle is already takne by other user, whether a uew handle could be generated correctly while the handle exceeding 20 character limit
'''

def test_register_handle_taken_and_long():

    clear()    
    data = load_data()
    curr_user_id1 = register("testhandle6@gmail.com", "123456", "Judypiggy", "Happysundaywoo")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id1['auth_user_id']:
            assert (user['handle_str'] == 'judypiggyhappysunday')
            
    curr_user_id2 = register("testhandle7@gmail.com", "987654", "Judypiggy", "Happysundaywoo")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id2['auth_user_id']:
            assert (user['handle_str'] == 'judypiggyhappysunda0')

    curr_user_id3 = register("testhandle8@gmail.com", "woabcd11", "Judypiggy", "Happysundaywoo")
    
    for user in data['users']:
        if user['u_id'] == curr_user_id3['auth_user_id']:
            assert (user['handle_str'] == 'judypiggyhappysunda1')

'''
test reset password
'''
def test_reset_not_regestered():
    clear() 
    with pytest.raises(src.error.InputError):
        request_reset("testreset@gmail.com")
#success case
def test_password_reset_success():
    clear()    
    
    user_register = register("testreset@gmail.com", "123456", "Judy", "Happy")
    #reset_code = None
    request_reset("testreset@gmail.com")
    
    data = load_data()
   
    reset_password(data['users'][0]['reset_code'], "1234abcd")
    
    logout(user_register['token'])
    user_login = login("testreset@gmail.com", "1234abcd") 
   
    assert user_login['auth_user_id'] == user_register['auth_user_id']

#password too short    
def test_password_reset_too_short():
    clear()    
    data = load_data()
    register("testreset@gmail.com", "123456", "Judy", "Happy")
    reset_code = None
    request_reset("testreset@gmail.com")
    
    for user in data['users']:
        if user['email'] == "testreset@gmail.com":
            reset_code = user['reset_code']
    
    with pytest.raises(src.error.InputError):
        reset_password(reset_code, "12")

#reset code invalid        
def test_password_reset_invalid_code():
    clear()    
    load_data()
    register("testreset@gmail.com", "123456", "Judy", "Happy")
    request_reset("testreset@gmail.com")
    
    with pytest.raises(src.error.InputError):
        reset_password('invalid', "1234abcd")