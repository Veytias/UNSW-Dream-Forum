# auth_implementation: allows user to register an account, login and logout
import src.error as error
import re
import random
import string
import hashlib
import jwt
from src.helper import load_data,save_data, check_token_valid
import src.config as config

PORT = config.port
# set secret for jwt
SECRET = "Sunshine"


# validating Email 
regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'

registered = []

'''
helper functions
'''
sessionId = 1000
# generate session id
def getNewSessionid():
    global sessionId
    sessionId += 1
    return sessionId
    
# generate a token for this session: an authorisation hash
def generate_token(newSessionId, u_id):
    encoded_jwt = jwt.encode({'session_id': newSessionId, 'user_id': u_id}, SECRET, algorithm= 'HS256')
    return encoded_jwt

# find the session through token
def retrieve_session(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms= ['HS256'])

    return decoded

'''
auth_login: Given a registered users' email and password and generates a valid token for the user to remain authenticated 
'''
def auth_login_v2(email, password):
    '''
    This function will receive user email and password as parameters.
    A token and an authentic user id will be returned
    
    Arguments:
        match_user = <class 'NoneType'> - check if the user has already registered, if not match user is None
        corr_pas = <class 'bool'> - check if the password is correct
        u_id = <class 'int'> - access the user id and return it

    
    Exceptions:
        InputError - Occurs when the password is incorrect
    	InputError - Email entered is not a valid email
        InputError - Email entered does not belong to a user
    
    Return Value:  
    	Returns <'token': token, 'auth_user_id': u_id> on <email == user['email'] and password == user['password']>
    '''
    
    data = load_data()
    # check the validity of email (if the email is invalid) 
    # InputError - Email entered is not a valid email
    if not (re.search(regex,email)):  
        raise error.InputError(description="This email address is invalid")  
    
    match_user = None
    corr_pass = False  # corr_pas = <class 'bool'> - check if the password is correct
    
    #check encrypted password
    enc_password = hashlib.sha256(password.encode()).hexdigest()
    

    for user in data['users']: 
    # correct password and email
        if email == user['email']:
            match_user = user
        # if the email is not registered
        # InputError - Email entered does not belong to a user
    if match_user is None:
        raise error.InputError(description="This email is not registered")
    
    if enc_password == match_user['password']: 
        corr_pass = True
        u_id = user['u_id']  # u_id = <class 'int'> - access the user id and return it
        # generate new session_id
        newSessionId = getNewSessionid()
        data['users'][u_id-1]['sessionList'].append(newSessionId)
            
    
    # if the password is incorrect
    # InputError - Occurs when the password is incorrect
    if corr_pass == False:
        raise error.InputError(description="Your password is incorrect, please try again")
        
    save_data(data)
    # Returns <return 'auth_user_id': u_id> on <email == user['email'] and password == user['password']>
    return {
        'auth_user_id': u_id,
        'token': generate_token(newSessionId, u_id),
    }


def auth_logout_v1(token):
    '''
    Given an active token, this function invalidates the token to log the user out. 
    If a valid token is given, and the user is successfully logged out, 
    it returns true, otherwise false.
    
    Arguments:
        data_struc = <class 'Dicttoinary'> - contain session_id
        tokenSessionid = <class 'int'> - get session id

    
    Exceptions:
        AccessError - Given token is invalid
    
    Return Value:  
    	Returns { is_success: True/False }
    '''
    data = load_data()
    
    check_token_valid(token)
    
    dataStruc = retrieve_session(token)
    tokenSessionid = dataStruc['session_id']
    
    for idx, user in enumerate(data['users']):
       
        for idx, session in enumerate(data['users'][idx]['sessionList']):
            #the user is successfully logged out, remove current session
            if session == tokenSessionid:
                data['users'][idx]['sessionList'].remove(tokenSessionid)
                user['loggedIn'] = False
                save_data(data)
                return {'is_success': True}
           
            
    return {'is_success': False}




def auth_register_v2(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password, create a new account for them 
    and return a new token for authentication in their session.
    
    Arguments:
        new_name_first = <class 'str'> - for removing white space and @
        new_name_last = <class 'str'> - for removing white space and @
        handle = <class 'str'> - store the concatenation for each user registering
        append_num = <class 'int'> - for appending the number at end of already existing handle
        user_num = <class 'int'> - used in the for loop of generating new handle while it has been taken
        u_id = <class 'int'> - access the user id and return it
        token = <class 'string'> - for token generation
        enc_password = <class 'string'> - generate encoded password

    
    Exceptions:
        InputError - Email entered is not a valid email
        InputError - Email entered has been registered
        InputError - Occurs when the length of password is less than 6
    	InputError - If first name length is less than 1 character or greater than 50 characters
        InputError - If last name length is less than 1 character or greater than 50 characters
    
    Return Value:  
        Returns <'token': token, 'auth_user_id': u_id> on <user first name, last name, email, password are valid and format correctly, user email is unused>
    '''
    
    data = load_data()
    
    # check the validity of email (if the email is invalid)
    # InputError - Email entered is not a valid email 
    if not (re.search(regex,email)):  
        raise error.InputError(description="This email address is invalid")  
    
    # check if the email is unused
    # InputError - Email entered has been registered
    for user in data['users'] : 
        if email == user['email']:
            raise error.InputError(description="This email has already been registered, please use another one")
    
    # check if the length of password is less than 6, if so, raise inputerror
    # InputError - Occurs when the length of password is less than 6
    if(len(password) < 6): 
        raise error.InputError(description="your password is too short, please reset password")
    
    # check the format of name_first
    # if the first name is too long or too short raise exception
    # InputError - If first name length is less than 1 character or greater than 50 characters
    if(len(name_first) < 1): 
        raise error.InputError(description="firstname entered is too short")
        
    elif (len(name_first) > 50):
        raise error.InputError(description="firstname entered is too long, do not exceed the 50-character length limit")
    
    # check the format of name_last
    # if the last name is too long or too short raise exception
    # InputError - If last name length is less than 1 character or greater than 50 characters
    if(len(name_last) < 1): 
        raise error.InputError(description="lastname entered is too short")
        
    elif (len(name_last) > 50):
        raise error.InputError(description="lastname entered is too long, do not exceed the 50-character length limit")
    
    # remove any whitespace or the '@' character from handle
    new_name_first = ""  # new_name_first = <class 'str'> - for removing white space and @
    for i in name_first:
        if i != " " and i != "@":
            new_name_first = new_name_first + i
    
    new_name_last = ""  # new_name_last = <class 'str'> - for removing white space and @
    for i in name_last:
        if i != " " and i != "@":
            new_name_last = new_name_last + i
            
    
    # A handle is generated that is the concatenation of a lowercase-only first name and last name 
    handle = new_name_first.lower() + new_name_last.lower()  # handle = <class 'str'> - store the concatenation for each user registering
    
    # cutoff the handle at 20 characters.(refer to number slicing method in https://www.pythonforbeginners.com/dictionary/python-slicing )  
    handle = handle[:20]
    
        
    # check if the handle is taken
    # forms a new handle that isn't already taken
    
    append_num = 0  # append_num = <class 'int'> - for appending the number at end of already existing handle
    user_num = len(data['users'])  # user_num = <class 'int'> - used in the for loop of generating new handle while it has been taken
    if user_num > 0:
        for user in data['users'] :
            if handle == user['handle_str'] and append_num != 0:
                handle = handle[:-len(str(append_num))]                
                handle += str(append_num)
                append_num += 1
            elif handle == user['handle_str'] and append_num == 0 and len(str(handle)) == 20:
                handle = handle[:-len(str(append_num))]                
                handle += str(append_num)
                append_num += 1
            elif handle == user['handle_str'] and append_num == 0 and len(str(handle)) < 20:                
                handle += str(append_num)
                append_num += 1              
            else:
                break
    
    u_id = len(data['users']) + 1  # u_id = <class 'int'> - access the user id and return it

    #generate permission_id
    if u_id == 1:
        permission_id = 1
    if u_id > 1:
        permission_id = 2
    # Passwords must be stored in an encrypted form
    enc_password = hashlib.sha256(password.encode()).hexdigest()
    
    newSessionId = getNewSessionid()
    #generate token
    token = generate_token(newSessionId, u_id)
    
    data['users'].append({
        'u_id': u_id,
        'token': token,
        'email': email, 
        'name_first': name_first, 
        'name_last': name_last, 
        'password': enc_password, 
        'handle_str': handle,
        'permission_id': permission_id,
        'sessionList': [newSessionId],
        'loggedIn' : True,
        'channels':[],
        'notifications':[],
        'reset_code': None,
        'profile_img_url': f"http://localhost:{PORT}/static/initial.jpg",
        'user_stats':{'channels_joined':[], 'dms_joined': [],'messages_sent':[]}
        })
    registered.append({
        'u_id': u_id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        })
    save_data(data)
   
    return {
        'auth_user_id': u_id,
        'token': token,
    }

def auth_passwordreset_request_v1(email):
    
    '''
    Given an email address, if the user is a registered user, 
    sends them an email containing a specific secret code.

    Arguments:
        match_user = <class 'bool'> - check if user has registered the email
        reset_code = <class 'str'> - generate reset code

    
    Exceptions:
        InputError - Email entered does not belong to a user
        
    
    Return Value:  
        Returns {}
    '''
    
    data = load_data()
    
    match_user = None

    for user in data['users']: 
    
        if email == user['email']:
            match_user = user
        # if the email is not registered
        # InputError - Email entered does not belong to a user
    if match_user is None:
        raise error.InputError(description="This email is not registered")
    
    #generate reset code
    reset_code = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    
    #update reset code
    for user in data['users']:
        if email == user['email']:
            user['reset_code'] = reset_code
    
    save_data(data)
    
    return {}


def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    Given a reset code for a user, 
    set that user's new password to the password provided

    Arguments:
        reset_valid = <class 'bool'> - check if reset_code is not a valid reset code
    
    Exceptions:
        InputError - the reset code is invalid
        InputError - Occurs when the length of password is less than 6
        
    
    Return Value:  
        Returns {}
    '''
    
    data = load_data()
    
    reset_valid = False
    # InputError - Occurs when the length of password is less than 6
    if(len(new_password) < 6): 
        raise error.InputError(description="your password is too short, please reset password")
     
    for user in data['users']:
        if user['reset_code'] == reset_code:
            
            reset_valid = True            
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            print(data['users'][0]['password'])
            user['reset_code'] = None
    
    if reset_valid == False:
        raise error.InputError(description= "the reset code is invalid.")
            
    
    save_data(data)
    
    return {}
        
    
