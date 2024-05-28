import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data
import re

import urllib.request
from PIL import Image
import os
import src.config as config
from src.dm import dm_list_v1
from datetime import datetime, timezone

PORT = config.port
# validating Email 
regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'

def user_profile_v2(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle

    Exceptions:
    InputError when any of: User with u_id is not a valid user

    Return Value:
    Returns <return dict(user)> on <u_id is already register to database>
    '''

    data = load_data()

    # InputError when any of: User with u_id is not a valid user
    if int(u_id) not in range(len(data['users']) + 1):
        raise error.InputError(description= "Invalid user.")

    check_token_valid(token)

    user = data['users'][int(u_id) - 1]

    return {
        'user': {
            'u_id': u_id,
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url'],
        }
    }

def user_profile_setname_v2(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    
    Exceptions:
    InputError when any of: name_first is not between 1 and 50 characters inclusively in length
    InputError when any of: name_last is not between 1 and 50 characters inclusively in length

    '''
    data = load_data()

    check_token_valid(token)

    u_id = getUserId(token)

    # InputError when any of: name_first is not between 1 and 50 characters inclusively in length
    if(len(name_first) < 1): 
        raise error.InputError(description= "firstname entered is too short")
        
    # InputError when any of: name_first is not between 1 and 50 characters inclusively in length
    elif (len(name_first) > 50):
        raise error.InputError(description= "firstname entered is too long, do not exceed the 50-character length limit")
    # InputError when any of: name_last is not between 1 and 50 characters inclusively in length
    if(len(name_last) < 1): 
        raise error.InputError(description= "lastname entered is too short")
    
    # InputError when any of: name_last is not between 1 and 50 characters inclusively in length
    elif (len(name_last) > 50):
        raise error.InputError(description= "lastname entered is too long, do not exceed the 50-character length limit")

    # do i need to u_id -1 ???
    data['users'][u_id - 1]['name_first'] = name_first
    data['users'][u_id - 1]['name_last'] = name_last

    save_data(data)
    return {
    }

def user_profile_setemail_v2(token, email):
    '''
    Update the authorized user's email address

    Exceptions:
    InputError when any of: Email entered is not a valid email
    InputError when any of: Email address is already being used by another user

    '''
    data = load_data()
    
    check_token_valid(token)

    u_id = getUserId(token)

    # check the validity of email (if the email is invalid) 
    # InputError - Email entered is not a valid email
    if not (re.search(regex,email)):  
        raise error.InputError(description= "This email address is invalid")
    
    # InputError when any of: Email address is already being used by another user
    for user in data['users']:
        if user['email'] == email:
            raise error.InputError(description= "This email has been taken.")
    
    data['users'][u_id - 1]['email'] = email

    save_data(data)
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)

    Exceptions:
    InputError when any of: handle_str is not between 3 and 20 characters inclusive
    InputError when any of: handle is already used by another user

    '''

    data = load_data()
    
    check_token_valid(token)

    u_id = getUserId(token)

    # InputError when any of: handle_str is not between 3 and 20 characters inclusive
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise error.InputError(description= "handle_str should be between 3 and 20 characters inclusive")
    
    # InputError when any of: handle is already used by another user
    for user in data['users']:
        if user['handle_str'] == handle_str:
            raise error.InputError(description= "This handle has been taken.")
            
    data['users'][u_id - 1]['handle_str'] = handle_str

    save_data(data)
    return {
    }

def users_all_v1(token):
    '''
    Returns a list of all users and their associated details
    '''

    data = load_data()
    
    check_token_valid(token)

    all_users = []

    for user in data['users']:

        user_details = {
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str'],
        'profile_img_url': user['profile_img_url'],
        }

        all_users.append(user_details)
    
    save_data(data)
    
    return {'users' : all_users}


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.

    Arguments:
        u_id = <class 'int'> - get u_id from token
        img_path = <class 'str'> - generate the image static path
        img_jpg = <class 'bool'> - check if image is jpg format
        crop_valid = <class 'bool'> - check if crop bounds are valid

    
    Exceptions:
        AccessError - Token invalid.
        InputError - img_url returns an HTTP status other than 200.
        InputError - any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
        InputError - Image uploaded is not a JPG
    
    Return Value:  
        Returns {}
    '''
    
    data = load_data()
    check_token_valid(token)

    u_id = getUserId(token)
    '''
    use request.urlopen from urllib.request ?? Extensible library for opening URLs
    try: 
        urllib.request.urlopen(img_url)
    except urllib.request.HTTPError as http_error:
        #img_url returns an HTTP status other than 200.
        raise error.InputError(description= "img_url invalid.") from http_error
    except ValueError as unknown_url_type:
        raise error.InputError(description= "img_url invalid.") from unknown_url_type
    '''


    img_path = f"{os.getcwd()}/src/static/{u_id}.jpg"
    try:
        urllib.request.urlretrieve(img_url, img_path) 
    except urllib.request.HTTPError as http_error:
        #img_url returns an HTTP status other than 200.
        raise error.InputError(description= "img_url invalid.") from http_error
    except ValueError as unknown_url_type:
        raise error.InputError(description= "img_url invalid.") from unknown_url_type
    
    img_jpg = False
    if img_url.lower().endswith('.jpg'):
        img_jpg = True 

    if img_jpg == False:
        raise error.InputError(description= "img is not jpg format.")

    #get the size of user image
    user_img = Image.open(img_path)
    width, height = user_img.size

    crop_valid = True
    if int(x_start) < 0 or int(x_start) >= int(x_end) or int(x_end) > int(width):
        crop_valid = False
    if int(y_start) < 0 or int(y_start) >= int(y_end) or int(y_end) > int(height):
        crop_valid = False

    #any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.
    if not crop_valid:
        os.remove(img_path)
        raise error.InputError(description= "Invalid crop bounds provided.")
    
    #crop and save image
    crop_image = user_img.crop((int(x_start), int(y_start), int(x_end), int(y_end)))
    crop_image.save(img_path)
    
    new_img_url = f"http://localhost:{PORT}/static/{u_id}.jpg"
    
    data['users'][u_id-1]['profile_img_url'] = new_img_url
    
    save_data(data)

    return {}
'''
keep track of the user involvement with UNSW dream
'''
def user_stats_v1(token):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dream_info> - <class 'list'> - <contain all messages, channels, and dms in UNSW Dream>
    <involvement rate> -  <class 'int'> - <percent of the user involvement with UNSW Dream>
    <new_time> - <class 'int'> - <update any changes to the user stat with timestamp>
    ...

    Exceptions:
    InputError  - None
    
    AccessError - None   

    Return Value:
    Returns <return dict(user_stats)>
    '''
    data = load_data()

    check_token_valid(token)
    u_id = getUserId(token)

    dream_message = len(data['messages'])

    num_channel_joined = len(data['users'][u_id-1]['channels'])
    dream_channels = len(data['channels'])

    user_dm = dm_list_v1(token)
    num_dm_joined = len(user_dm['dms'])
    dream_dms = len(data['dms'])

    message_count = 0
    for message in data['messages']:
        if message['u_id'] == u_id:
            message_count+=1
    
    for dm in data['dms']:
        dream_message+=len(dm['messages'])
        for message_dm in dm['messages']:
            if message_dm['u_id'] == u_id:
                message_count+=1
    
    dream_info = [dream_channels, dream_dms, dream_message]

    involvement_rate = sum([num_channel_joined, num_dm_joined, message_count])/sum(dream_info)
    
    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    new_time = int(timestamp)
    
    stat = data['users'][u_id-1]['user_stats']

    channel_stat = 0
    dm_stat = 0
    msg_stat = 0
    if len(stat['channels_joined']) != 0:
        channel_stat = stat['channels_joined'][-1]['num_channels_joined']
    if len(stat['dms_joined']) != 0:
        dm_stat = stat['dms_joined'][-1]['num_dms_joined']
    if len(stat['messages_sent']) != 0:
        msg_stat = stat['messages_sent'][-1]['num_messages_sent']

    # Check if channel join change
    if channel_stat != num_channel_joined or len(stat['channels_joined']) == 0:
        new_ch_stat = {'num_channels_joined': num_channel_joined, 'time_stamp': new_time}
        stat['channels_joined'].append(new_ch_stat)

    # Check if dm join change
    if dm_stat != num_dm_joined or len(stat['dms_joined']) == 0:
        new_dm_stat = {'num_dms_joined': num_dm_joined, 'time_stamp': new_time}
        stat['dms_joined'].append(new_dm_stat)
    
    # Check if message sent change
    if msg_stat !=  message_count or len(stat['messages_sent']) == 0:
        new_msg_stat = {'num_messages_sent': message_count, 'time_stamp': new_time}
        stat['messages_sent'].append(new_msg_stat)

    save_data(data)

    new_dict = data['users'][u_id-1]['user_stats']
    new_dict['involvement_rate'] = involvement_rate
    
    return  {'user_stats': new_dict}

'''
keep track of all messages, channels, and dms that exist in dream and give utilization rate
'''
def users_stats_v1(token):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <util_rate> -  <class 'int'> - <percent of the messages, channels, and dms that are use by users in UNSW dream>
    <new_time> - <class 'int'> - <update any changes to the dream stat with timestamp>
    ...

    Exceptions:
    InputError  - None
    
    AccessError - None   

    Return Value:
    Returns <return dict(dreams_stats)>
    '''
    data = load_data()

    check_token_valid(token)
    getUserId(token)

    num_channel_exist = len(data['channels'])
    num_dms_exist = len(data['dms'])
    num_messages_exist = len(data['messages'])
    num_user_exist = len(data['users'])

    for dm in data['dms']:
        num_messages_exist+=len(dm['messages'])

    user_joined = 0
    for user in data['users']:
        if len(user['channels']) != 0:
            user_joined+=1
        else:
            for dm in data['dms']:
                for dm_mem in dm['dm_members']:
                    if user['u_id'] == dm_mem['u_id']:
                        user_joined+=1

    util_rate = user_joined/num_user_exist

    stat = data['dreams_stats']

    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    new_time = int(timestamp)

    ch_stat = 0
    dm_stat = 0
    msg_stat = 0

    if len(stat['channels_exist']) != 0:
        ch_stat = stat['channels_exist'][-1]['num_channels_exist']

    if len(stat['dms_exist']) != 0:
        dm_stat = stat['dms_exist'][-1]['num_dms_exist']

    if len(stat['messages_exist']) != 0:
        msg_stat = stat['messages_exist'][-1]['num_messages_exist']

    # Check if channel exist change
    if ch_stat != num_channel_exist or len(stat['channels_exist']) == 0:
        new_ch_stat = {'num_channels_exist': num_channel_exist, 'time_stamp': new_time}
        stat['channels_exist'].append(new_ch_stat)

    # Check if dm exist change
    if dm_stat != num_dms_exist or len(stat['dms_exist']) == 0:
        print(num_dms_exist)
        new_dm_stat = {'num_dms_exist': num_dms_exist, 'time_stamp': new_time}
        stat['dms_exist'].append(new_dm_stat)
    
    # Check if message exist change
    if msg_stat !=  num_messages_exist or len(stat['messages_exist']) == 0:
        new_msg_stat = {'num_messages_exist': num_messages_exist, 'time_stamp': new_time}
        stat['messages_exist'].append(new_msg_stat)

    
    save_data(data)

    new_dict = data['dreams_stats']
    new_dict['utilization_rate'] = util_rate

    return  {'dreams_stats': new_dict}


