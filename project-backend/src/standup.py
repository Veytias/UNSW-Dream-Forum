import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data
import threading
from datetime import datetime, timedelta, timezone

'''
help functions
'''


def select_channel(channel_id):
    data = load_data()
    BEGIN = 0
    channel_order = BEGIN
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel_order
        channel_order += 1
    return False

#check if the user is a member of a channel
def check_member_ch(u_id, channel_id):
    data = load_data()

    for member in data['channels'][channel_id-1]['all_members']:
        if u_id == member['u_id']:
            return True
    return False

def standup_close(token, channel_id, standup_id):
    data = load_data()
    u_id = getUserId(token)

    wrapper = []
    for standup in data['standups']:
        if standup['standup_id'] == standup_id:
            for message in standup['messages']:
                wrapper.append(f"{message['name_first']}: {message['message']}")
    wrapper = '\n'.join(wrapper)

    t = datetime.now()
    curr_finish = t.replace(tzinfo=timezone.utc).timestamp()

    count = 0
    for dms in data['dms']:
            count+=len(dms['messages'])

    msg_id = len(data['messages']) + count + 1
    data['messages'].append({
        'message_id': msg_id,
        'channel_id' : channel_id,
        'u_id': u_id,
        'message': wrapper,
        'time_created': int(curr_finish),
    })
    save_data(data)

'''
main functions
'''

'''
For a given channel, start the standup period whereby for the next "length" seconds if someone calls 
"standup_send" with a message, it is buffered during the X second window then at the end of the X second 
window a message will be added to the message queue in the channel from the user who started the standup. 
X is an integer that denotes the number of seconds that the standup occurs for
'''
def standup_start(token, channel_id, length):
    '''
    Arguments:
    <channel_index> (<class 'int'>)    - <check  channel_id existance>
    <channel_exist> (<class 'bool'>)    - <check given channel_id existance>
    <inChannel> (<class 'bool'>)    - <check given u_id existance>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when standup in the given channel is currently running
    AccessError - Occurs when authorized user is not a member of the given channel_id

    Return Value:
    Returns <return dict(time_finish)> on <user_access == True && channel_exist is exist && standp is not currently running>
    '''
    channel_exist = False

    #access database
    data = load_data()
    
    check_token_valid(token)

    # check whether the input channel exist or not 
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True
        #channel = data['channels'][channel_index]

    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    # InputError - Occurs when an active standup is currently running in this channel
    if standup_active(token, channel_id)['is_active'] == True:
        raise error.InputError(description= "Error, {channel_id}'s standup is currently active")

    auth_id = getUserId(token)

    inChannel = check_member_ch(auth_id, channel_id)

    # AccessError - Occurs when authorised user is not in the channel
    if inChannel == False:
        raise error.AccessError(description="the authorized user haven't joined this channel")    

    # datetime object containing current date and time
    now = datetime.now()
    finish_time = (now + timedelta(seconds=length)).timestamp()

    standup_id = len(data['standups'])+1

    data['standups'].append({'standup_id' : standup_id, 
                             'channel_id' : channel_id,
                             'time_finish' : int(finish_time),
                             'messages' : []})
    save_data(data)

    # set stand_up status to false after 'length' seconds has past
    t = threading.Timer(length, standup_close, args=[token, channel_id, standup_id])
    t.start()

    return {'time_finish': int(finish_time)}

'''
For a given channel, return whether a standup is active in it, and what time the standup finishes. 
If no standup is active, then time_finish returns None
'''
def standup_active(token, channel_id):
    '''
    Arguments:
    <channel_index> (<class 'int'>)    - <check  channel_id existance>
    <channel_exist> (<class 'bool'>)    - <check given channel_id existance>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when standup in the given channel is currently running

    Return Value:
    Returns <return dict(is_active, time_finish)> on <channel_exist is exist>
    '''
    channel_exist = False
     
    #access database
    data = load_data()
    
    check_token_valid(token)

    # check whether the input channel exist or not    
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True

    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    for stdup in data['standups']:
        
        t = datetime.now().timestamp()
        if t < stdup['time_finish'] and channel_id == stdup['channel_id']:
            time = stdup['time_finish']

            return {'is_active': True, 'time_finish': int(time)}
    
    return {'is_active': False, 'time_finish': None}

'''
Sending a message to get buffered in the standup queue, assuming a standup is currently active
'''
def standup_send(token, channel_id, message):
    '''
    Arguments:
    <channel_index> (<class 'int'>)    - <check  channel_id existance>
    <channel_exist> (<class 'bool'>)    - <check given channel_id existance>
    <inChannel> (<class 'bool'>)    - <check given u_id existance>
    <is_active> (<class 'bool'>)    - <check if give channel's standup is currenlt running>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    InputError  - Occurs when standup in the given channel is currently running
    InputError  - Occurs when length of message is larger than 1000 characters
    AccessError - Occurs when authorized user is not a member of the given channel_id
    '''
    channel_exist = False

    #access database
    data = load_data()
    
    check_token_valid(token)

    # check whether the input channel exist or not    
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True

    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    # InputError - Occurs when message is more than 1000 characters
    if len(message) > 1000:
        raise error.InputError(description= "Message is more than 1000 characters")

    is_active = False
    for stdup in data['standups']:
        t = datetime.now().timestamp()
        if t < stdup['time_finish'] and channel_id == stdup['channel_id']:
            is_active = True
            target_stdup = stdup

    # InputErrir - Occur when an active standup is not currently running in this channel
    if not is_active:
        raise error.InputError(description= "An active standup is not currently running in this channel")

    auth_id = getUserId(token)

    inChannel = check_member_ch(auth_id, channel_id)
    
    # AccessError - Occurs when authorised user is not in the channel
    if inChannel == False:
        raise error.AccessError(description="the authorized user haven't joined this channel")
    
    for user in data['users']:
        if user['u_id'] == auth_id:
            name_first = user['name_first']
    
    target_stdup['messages'].append({'name_first': name_first, 'message' : message, 'u_id' : auth_id})
    save_data(data)

    return {}

