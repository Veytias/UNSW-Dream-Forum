from src.helper import getUserId,check_token_valid,load_data,save_data
import src.error as error
import time
import threading

'''
helper functions
'''
SECRET = "Sunshine"

# Find dm index of the given dm_id
def select_dm(dm_id):
    data = load_data()
    BEGIN = 0
    dm_order = BEGIN
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return dm_order
        dm_order += 1
    return False
        
def select_channel(channel_id):
    data = load_data()
    BEGIN = 0
    channel_order = BEGIN
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel_order
        channel_order += 1
    return False
    
def find_msg_index_dm(message_id):
    data = load_data()

    for dm in data['dms']:
        msg_index = 0
        for message in dm['messages']:
            if message['message_id'] == message_id:
                return msg_index
            msg_index+=1

def find_msg_index_ch(message_id):
    data = load_data()
    msg_index = 0
    for message in data['messages']:      
        if message['message_id'] == message_id:
            return msg_index
        msg_index+=1          
# check if the message_id passed in is valid, if valid return the channel id it is in
def check_message_id_valid(message_id):
    data = load_data()
    msg_index = 0
    message_id_valid = True

    if message_id == None:
        message_id_valid = False

    for message in data['messages']:
        if message['message_id'] == message_id:
            channel_id = message['channel_id']
            return {'message_id_valid': message_id_valid, 'channel_id': channel_id, 'msg_index': msg_index}
        msg_index+=1
        
    return {'message_id_valid': False, 'channel_id': None}
    
# check if the message_id passed in is valid, if valid return the channel id it is in
def check_message_id_valid_all_dm(message_id):
    data = load_data()
    message_id_valid = True

    if message_id == None:
        message_id_valid = False

    for dm in data['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm_id = dm['dm_id']
                return {'message_id_valid': message_id_valid, 'dm_id': dm_id}
   
    return {'message_id_valid': False, 'dm_id': None}    

# check if message_id is valid, if valid return the dm id it is in
def check_message_id_valid_dm(message_id, dm_id):
    global SECRET
    data = load_data()

    message_id_valid = False

    if message_id == None:
        message_id_valid = False

    dm_index = select_dm(dm_id)
    for message in data['dms'][dm_index]['messages']:
        if message['message_id'] == message_id:
            message_id_valid = True
            return {'message_id_valid': message_id_valid}
        
    return {'message_id_valid': message_id_valid}


#check if the user is the owner_member of a channel
def check_if_user_owner(u_id, channel_id):
    data = load_data()
    valid = False
    for owner in data['channels'][channel_id-1]['owner_members']:
        if u_id == owner['u_id']:
            valid = True
    return valid

#check if the user is the owner_member of a dm
def check_if_user_owner_dm(u_id, dm_id):
    data = load_data()
    valid = False
    
    dm_index = select_dm(dm_id)
    if data['dms'][dm_index]['dm_owner'] == u_id:
        valid = True

    return valid  

#check if the user is a member of a channel
def check_member_ch(u_id, channel_id):
    data = load_data()

    for member in data['channels'][channel_id-1]['all_members']:
        if u_id == member['u_id']:
            return True
    return False

#check if the user is a member of a dm
def check_member_dm(u_id, dm_id):
    data = load_data()

    dm_index = select_dm(dm_id)
    for member in data['dms'][dm_index]['dm_members']:
        if u_id == member['u_id']:
            return True
    return False

def get_dm_id(message_id):
    data = load_data()

    for dms in data['dms']:
        for msg in dms['messages']:
            if msg['message_id'] == message_id:
                dm_id = msg['dm_id']
                return {'message_id_valid': True, 'dm_id': dm_id}

    return {'message_id_valid': False, 'dm_id': None}
    
def get_uid_from_handle(handle):
    data = load_data()
    for user in data['users']:
        if handle == user['handle_str']:
            return user['u_id']
    return None   
    
def notifications_tag_ch(auth_id, channel_id, message):
    data = load_data()
    message_list = message.split()
    auth_handle = data['users'][auth_id -1]['handle_str']
    for word in message_list:
        if '@' in word:
            handle = word[1:]
            u_id = get_uid_from_handle(handle)
            user_in_ch = check_member_ch(u_id, channel_id)        
            if u_id != None and user_in_ch  == True:
                ch_index = select_channel(channel_id)
                channel_name = data['channels'][ch_index]['name']
                noti_message = f"{auth_handle} tagged you in {channel_name}: {message[:20]}"
                data['users'][u_id - 1]['notifications'].append({'channel_id':channel_id, 'dm_id': -1, 'notification_message':noti_message})
    save_data(data)
def notifications_tag_dm(auth_id, dm_id, message):
    data = load_data()
    message_list = message.split()
    auth_handle = data['users'][auth_id -1]['handle_str']
    for word in message_list:
        if '@' in word:
            handle = word[1:]
            u_id = get_uid_from_handle(handle)
            user_in_dm = check_member_dm(u_id,dm_id)        
            if u_id != None and user_in_dm == True:
                dm_index = select_dm(dm_id)
                dm_name = data['dms'][dm_index]['dm_name']
                noti_message = f"{auth_handle} tagged you in {dm_name}: {message[:20]}"
                data['users'][u_id - 1]['notifications'].append({'channel_id': -1, 'dm_id': dm_id, 'notification_message':noti_message})             
    save_data(data)
def notifications_react_ch(auth_id, message_id, channel_id):
    data = load_data()
    msg_index = find_msg_index_ch(message_id)
    auth_handle = data['users'][auth_id -1]['handle_str']
    u_id = data['messages'][msg_index]['u_id']
    ch_index = select_channel(channel_id)
    channel_name = data['channels'][ch_index]['name']    
    noti_message = f"{auth_handle} reacted to your message in {channel_name}"
    data['users'][u_id - 1]['notifications'].append({'channel_id': channel_id, 'dm_id': -1, 'notification_message':noti_message})
    save_data(data)
def notifications_react_dm(auth_id, message_id, dm_id):
    data = load_data()
    msg_index = find_msg_index_dm(message_id)
    auth_handle = data['users'][auth_id -1]['handle_str']
    dm_index = select_dm(dm_id)
    u_id = data['dms'][dm_index]['messages'][msg_index]['u_id']
    dm_name = data['dms'][dm_index]['dm_name']    
    noti_message = f"{auth_handle} reacted to your message in {dm_name}"
    data['users'][u_id - 1]['notifications'].append({'channel_id': -1, 'dm_id': dm_id, 'notification_message':noti_message})     
    save_data(data)   
def message_send_v2(token, channel_id, message):
    '''
    Send a message from authorized_user to the channel specified by channel_id.
    
    Arguments:
        u_id = <class 'int'> - access the user id
        InChannel = <class 'Bool'> - check if the user in in the channel
        newMessageId = <class 'int'> - generate message id start from 1
        now = <class 'string'> - generate datetime

    
    Exceptions:
        AccessError - Given token is invalid
        AccessError - user haven't join channel
        InputError - length of message > 1000        
    
    Return Value:  
        Returns { message_id: NewMessageId }
    '''
    data = load_data()
    
    if channel_id == None or channel_id < 0:
        raise error.AccessError(description="Channelid invalid.")
    check_token_valid(token)

    u_id =  getUserId(token)

    inChannel = check_member_ch(u_id, channel_id)

    if inChannel == False:
        raise error.AccessError(description="the authorized user haven't joined this channel")

    #raise inputError
    if len(message) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")
    
    count = 0
    for dms in data['dms']:
        count+=len(dms['messages'])

    newMessageId = len(data['messages']) + count + 1
    
    
    # datetime object containing current date and time
    timestamp = int(time.time())

    data['messages'].append({
        'message_id': newMessageId,
        'channel_id' : channel_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp,
        'reacts':[{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
        'is_pinned': False,
    })
    save_data(data)
    notifications_tag_ch(u_id, channel_id, message)
    data = load_data()
    save_data(data)
    return {
        'message_id': newMessageId,
    }

def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel/DM.

    Arguments:
        u_id = <class 'int'> - access the user id
        check_m = <class 'dict'> - check message_id valid and get channel_id
        check_m2 = <class 'dict'> - check message_id valid and get dm_id
        dm_index =  <class 'int'> - access the dm index

    Exceptions:
        AccessError - Given token is invalid
        AccessError - user haven't join channel or DM
        InputError - message no longer exists      

    Return Value:  
        Returns {}
    '''
    data = load_data()
    
    #check token valid
    check_token_valid(token)
   
    u_id =  getUserId(token)
    user = data['users'][u_id - 1]

    #check message_id valid
    check_m = check_message_id_valid(message_id)
    check_m2 = get_dm_id(message_id)

    if check_m['message_id_valid'] == False and check_m2['message_id_valid'] == False:
        raise error.InputError(description= "Message_id invalid")

    #find the message sender and content through message_id
    if check_m['message_id_valid'] == True:
        for message in data['messages']:
            if message['message_id'] == message_id:    
                mid = message['u_id']

        # check if user has authority to delete the message
        if user['u_id'] != mid and check_if_user_owner(u_id, check_m['channel_id']) == False and user['u_id'] != 1:
            raise error.AccessError(description="You are not the sender of this message or the owner member of this channel")
        else:
            for message in data['messages']:
                if message['message_id'] == message_id:
                    data['messages'].remove(message)


    if check_m2['message_id_valid'] == True:
        for dms in data['dms']:
            for msg in dms['messages']:
                if msg['message_id'] == message_id:
                    mid_dm = msg['u_id']
        
        
        if user['u_id'] != mid_dm and check_if_user_owner_dm(u_id, check_m2['dm_id']) == False and user['u_id'] != 1:
            raise error.AccessError(description="You are not the sender of this message or the owner member of this dm")    
        else:
            dm_index = select_dm(check_m2['dm_id'])

            for message in data['dms'][dm_index]['messages']:     
                if message['message_id'] == message_id:
                    data['dms'][dm_index]['messages'].remove(message)
           
    save_data(data)

    return {
    }

def message_edit_v2(token, message_id, message):
    '''
    Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

    Arguments:
        u_id = <class 'int'> - access the user id
        check_m = <class 'dict'> - check message_id valid and get channel_id
        check_m2 = <class 'dict'> - check message_id valid and get dm_id
        dm_index =  <class 'int'> - access the dm index

    Exceptions:
        AccessError - Given token is invalid
        AccessError - user haven't join channel or DM
        InputError - message no longer exists
        InputError - length of message > 1000    

    Return Value:  
        Returns {}
    '''

    data = load_data()

    #check token valid
    check_token_valid(token)
    #raise inputError
    if len(message) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")
        
    u_id =  getUserId(token)
    user = data['users'][u_id-1]

    #check message_id valid
    check_m = check_message_id_valid(message_id)
    check_m2 = get_dm_id(message_id)

    if check_m['message_id_valid'] == False and check_m2['message_id_valid'] == False:
        raise error.InputError(description= "Message_id invalid")

    #find the message sender and content through message_id
    if check_m['message_id_valid'] == True:
        for m in data['messages']:
            if m['message_id'] == message_id:    
                mid = m['u_id']

        # check if user has authority to delete the message
        if user['u_id'] != mid and check_if_user_owner(u_id, check_m['channel_id']) == False and user['u_id'] != 1:
            raise error.AccessError(description="You are not the sender of this message or the owner member of this channel")
        else:
            for mess in data['messages']:
                if mess['message_id'] == message_id:
                    mess['message'] = message
                    save_data(data)
                    notifications_tag_ch(u_id, check_m['channel_id'], message)
                    data = load_data()
    

    if check_m2['message_id_valid'] == True:
        for dms in data['dms']:
            for msg in dms['messages']:
                if msg['message_id'] == message_id:
                    mid_dm = msg['u_id']

        print(check_if_user_owner_dm(u_id, check_m2['dm_id']))
        if user['u_id'] != mid_dm and check_if_user_owner_dm(u_id, check_m2['dm_id']) == False and user['u_id'] != 1:
            raise error.AccessError(description="You are not the sender of this message or the owner member of this dm")    
        else:
            dm_index = select_dm(check_m2['dm_id'])

            for mess2 in data['dms'][dm_index]['messages']:     
                if mess2['message_id'] == message_id:
                    mess2['message'] = message
                    save_data(data)
                    notifications_tag_dm(u_id, check_m2['dm_id'], message)
                    data = load_data()
    save_data(data)

    return {
    }
'''
Send a message from authorized_user to the dm specified by dm_id
'''
def message_senddm_v1(token, dm_id, message):    
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_member_valid> - <class 'bool'> - <check if token is member of dm_id>
    ...

    Exceptions:
    InputError - Occurs when Message is more than 1000 characters         
    AccessError - Occurs when the authorised user is not a member of the DM they are trying to post to

    Return Value:
    Returns <return dict(message_id)> on <dm_member_valid == True && message <= 1000>
    '''

    data = load_data()
    
    check_token_valid(token)

    u_id =  getUserId(token)
    
    if dm_id == None:
        raise error.InputError(description="Given dm_id is invalid")

    dm_member_valid = check_member_dm(u_id, dm_id)

    #raise Accesserror
    if dm_member_valid == False:
        raise error.AccessError(description="the authorized user haven't joined this dm")

    #raise inputError
    if len(message) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")

    count = 0
    for dms in data['dms']:
        count+=len(dms['messages'])

    newMessageId = len(data['messages']) + count + 1
    # datetime object containing current date and time
    timestamp = int(time.time())
    
    dm_index = select_dm(dm_id)
    
    data['dms'][dm_index]['messages'].append({
        'message_id': newMessageId,
        'dm_id': dm_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp,
        'reacts':[{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
        'is_pinned': False,
    })
    save_data(data)
    notifications_tag_dm(u_id, dm_id, message)
    data = load_data()
    save_data(data)
    return {
        'message_id': newMessageId,
    }

'''
share message to a channel or dm with og_message_id plus additional message if any
'''
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <og_valid_ch> - <class 'bool'> - <check given og_message id is valid in channel>
    <og_valid_dm> -  <class 'bool'> - <check given og_message id is valid in dm>
    ...

    Exceptions:
                 
    AccessError - Occurs when the authorised user has not joined the channel or 
                DM they are trying to share the message to

    Return Value:
    Returns <return dict(shared_message_id)> on <og_valid_ch == True or og_valid_dm == True>
    '''

    #check token valid
    check_token_valid(token)

    auth_user = getUserId(token)

    data = load_data()

    #check og_message_id in channel
    if dm_id == -1:
        og_valid_ch = check_message_id_valid(og_message_id)
    
        if og_valid_ch['message_id_valid'] == False:
            raise error.InputError(description="og_message_id invalid.")

        message_index = check_message_id_valid(og_message_id)
        og_message = data['messages'][message_index['msg_index']]['message']

        share_message = og_message + " " + message

        if check_member_ch(auth_user, channel_id) == False:
            raise error.AccessError(description="user is not a member of the channel.")

        m_id = message_send_v2(token, channel_id, share_message)
        save_data(data)
        notifications_tag_ch(auth_user, channel_id, share_message)
        data = load_data()
        save_data(data)
        return { 'shared_message_id': m_id['message_id'] }

    if channel_id == -1:
        og_valid_dm = check_message_id_valid_dm(og_message_id, dm_id)

        if og_valid_dm['message_id_valid'] == False:
            raise error.InputError(description="og_message_id invalid.")

        message_index = find_msg_index_dm(og_message_id)
        dm_index = select_dm(dm_id)
        og_message = data['dms'][dm_index]['messages'][message_index]['message']

        share_message = og_message + " " + message

        if check_member_dm(auth_user, dm_id) == False:
            raise error.AccessError(description="user is not a member of the dm.") 
            
        m_id = message_senddm_v1(token, dm_id, share_message)
        save_data(data)
        notifications_tag_dm(auth_user, dm_id, share_message)
        data = load_data()
        save_data(data)
        return { 'shared_message_id': m_id['message_id'] }

'''
send message to a channel after a specified time delay
'''        
def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_exist> - <class 'bool'> - <check if the given channel_id exist>
    <time_sent> -  <class 'int'> - <tell the time delay as in seconds>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
                - Occurs when message exceeds 1000 characters
                - Occurs when time_sent is negative
    AccessError - Occurs when user is not a member of the channel      

    Return Value:
    Returns <return dict(message_id)> on <channel_exist == True && time_sent >= 0 >
    '''
    channel_exist = False
    
    check_token_valid(token)
    auth_user = getUserId(token)

    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True

    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    if len(message) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")

    if time_sent < 0:
        raise error.InputError(description="Time sent is a time in the past")

    if check_member_ch(auth_user, channel_id) == False:
        raise error.AccessError(description="user is not a member of the channel.") 

    time.sleep(time_sent)
    mess_id = message_send_v2(token,channel_id,message)

    return {'message_id': mess_id['message_id']}

'''
send message to a dm after a specified time delay
'''
def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_exist> - <class 'bool'> - <check if the given dm exist>
    <time_sent> -  <class 'int'> - <tell the time delay as in seconds>
    ...

    Exceptions:
    InputError  - Occurs when given dm_id does not exist
                - Occurs when message exceeds 1000 characters
                - Occurs when time_sent is negative
    AccessError - Occurs when user is not a member of the dm     

    Return Value:
    Returns <return dict(message_id)> on <dm_exist == True && time_sent >= 0 >
    '''
    dm_exist = False
    
    check_token_valid(token)
    auth_user = getUserId(token)

    dm_index = select_dm(dm_id)
    if dm_index is not False:
        dm_exist = True

    if dm_exist == False:
        raise error.InputError(description= "Error, {dm_id} is not valid")

    if len(message) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")

    if time_sent < 0:
        raise error.InputError(description="Time sent is a time in the past")

    if check_member_dm(auth_user, dm_id) == False:
        raise error.AccessError(description="user is not a member of the dm.") 

    time.sleep(time_sent)
    mess_id = message_senddm_v1(token,dm_id,message)
    
    return {'message_id': mess_id['message_id']}



def message_react_v1(token, message_id, react_id):
    '''
    Given a message_id for a message, react this message.
    
    Arguments:
        u_id = <class 'int'> - access the user id
        valid_message = <class 'Bool'> - check if the message valid
        message_id_valid_ch = <class 'dict'> check the message is in channel, if it is then return channel id
        message_id_valid_dm = <class 'dict'> check the message is in dm, if it is then return dm id
        is_reacted = <class 'bool'> - check is this message has been reacted or not


    
    Exceptions:
        AccessError - The authorised user is not a member of the channel or DM that the message is within
        InputError - message id is not valid
        InputError - react id is not valid
        InputError - message already been reacted       
    
    Return Value:  
        Returns {}
    '''
    #check token valid
    check_token_valid(token)
    u_id = getUserId(token)
    data = load_data()    
    #
    valid_message = False
    message_id_valid_ch = check_message_id_valid(message_id)
    message_id_valid_dm = check_message_id_valid_all_dm(message_id)
    if message_id_valid_ch['message_id_valid'] == True:
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == True:
            valid_message = True
        else:
            raise error.AccessError(description = 'The authorised user is not a member of the channel that the message is within')
    elif message_id_valid_dm['message_id_valid'] == True:
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == True:
            valid_message = True
        else:
            raise error.AccessError(description = 'The authorised user is not a member of the dm that the message is within')    
    if valid_message == False:
        raise error.InputError(description = 'message_id is not a valid message within a channel or DM that the authorised user has joined.') 
    #
    if react_id != 1:
        raise error.InputError(description = f'{react_id} is not a valid React ID')   
    #
    is_reacted = True
    if message_id_valid_ch['message_id_valid'] == True:  
        message_index = find_msg_index_ch(message_id)
        for react in data['messages'][message_index]['reacts']:
            if u_id not in react['u_ids']:
        	    is_reacted = False
        	    react['u_ids'].append(u_id)
        	    react['is_this_user_reacted'] = True
        	    channel_id = message_id_valid_ch['channel_id']
        	    save_data(data)
        	    notifications_react_ch(u_id, message_id, channel_id)
        	    data = load_data()
    else:
        message_index = find_msg_index_dm(message_id)
        dm_index = select_dm(message_id_valid_dm['dm_id'])
        for react in data['dms'][dm_index]['messages'][message_index]['reacts']:
        	if u_id not in react['u_ids']:
        	    is_reacted = False
        	    react['u_ids'].append(u_id)
        	    react['is_this_user_reacted'] = True
        	    dm_id = message_id_valid_dm['dm_id']
        	    save_data(data)
        	    notifications_react_dm(u_id, message_id, dm_id)  
        	    data = load_data()      
    if is_reacted == True:
        raise error.InputError(description = f'Message with ID {message_id} already contains an active React with ID {react_id} from the authorised user') 
    save_data(data)
    return {}

def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message_id for a message, unreact this message.
    
    Arguments:
        u_id = <class 'int'> - access the user id
        valid_message = <class 'Bool'> - check if the message valid
        message_id_valid_ch = <class 'dict'> check the message is in channel, if it is then return channel id
        message_id_valid_dm = <class 'dict'> check the message is in dm, if it is then return dm id
        is_reacted = <class 'bool'> - check is this message has been unreacted or not


    
    Exceptions:
        AccessError - The authorised user is not a member of the channel or DM that the message is within
        InputError - message id is not valid
        InputError - react id is not valid
        InputError - message already been unreacted       
    
    Return Value:  
        Returns {}
    '''
    #check token valid
    check_token_valid(token)
    u_id = getUserId(token)
    data = load_data()    
    #
    valid_message = False
    message_id_valid_ch = check_message_id_valid(message_id)
    message_id_valid_dm = check_message_id_valid_all_dm(message_id)
    if message_id_valid_ch['message_id_valid'] == True:
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == True:
            valid_message = True
        else:
            raise error.AccessError(description = 'The authorised user is not a member of the channel that the message is within')
    elif message_id_valid_dm['message_id_valid'] == True:
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == True:
            valid_message = True
        else:
            raise error.AccessError(description = 'The authorised user is not a member of the dm that the message is within')   
    if valid_message == False:
        raise error.InputError(description = 'message_id is not a valid message within a channel or DM that the authorised user has joined.') 
    #
    if react_id != 1:
        raise error.InputError(description = f'{react_id} is not a valid React ID')   
    #
    is_reacted = False
    if message_id_valid_ch['message_id_valid'] == True:  
        message_index = find_msg_index_ch(message_id)
        for react in data['messages'][message_index]['reacts']:
            if u_id in react['u_ids']:
        	    is_reacted = True
        	    react['u_ids'].remove(u_id)
        	    react['is_this_user_reacted'] = False
    else:
        message_index = find_msg_index_dm(message_id)
        dm_index = select_dm(message_id_valid_dm['dm_id'])
        for react in data['dms'][dm_index]['messages'][message_index]['reacts']:
            if u_id in react['u_ids']:
        	    is_reacted = True
        	    react['u_ids'].remove(u_id)
        	    react['is_this_user_reacted'] = False
    if is_reacted == False:
        raise error.InputError(description = f'Message with ID {message_id} does not contain an active React with ID {react_id} from the authorised user')  
    save_data(data)
    return {}

def message_pin_v1(token, message_id):
    '''
    Given a message_id for a message, pin this message.
    
    Arguments:
        u_id = <class 'int'> - access the user id
        valid_message = <class 'Bool'> - check if the message valid
        message_id_valid_ch = <class 'dict'> check the message is in channel, if it is then return channel id
        message_id_valid_dm = <class 'dict'> check the message is in dm, if it is then return dm id
        is_pinned = <class 'bool'> - check is this message has been pinned or not


    
    Exceptions:
        AccessError - The authorised user is not a member of the channel or DM that the message is within
        AccessError - The authorised user is not an owner of the channel or DM
        InputError - message_id is not valid
        InputError - message already been pinned    
    
    Return Value:  
        Returns {}
    '''
    #check token valid
    check_token_valid(token)
    u_id = getUserId(token)
    data = load_data()    
    #
    valid_message = False
    message_id_valid_ch = check_message_id_valid(message_id)
    message_id_valid_dm = check_message_id_valid_all_dm(message_id)
    if message_id_valid_ch['message_id_valid'] == True:
        #
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == False:
            raise error.AccessError(description = 'The authorised user is not a member of the channel that the message is within')
        #
        if check_if_user_owner(u_id, message_id_valid_ch['channel_id']) == False:
            raise error.AccessError(description = 'The authorised user is not an owner of the channel')
        #        
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == True:
            valid_message = True    
    elif message_id_valid_dm['message_id_valid'] == True:
        #
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == False:
            raise error.AccessError(description = 'The authorised user is not a member of the dm that the message is within') 
        #
        if check_if_user_owner_dm(u_id, message_id_valid_dm['dm_id']) == False:
            raise error.AccessError(description = 'The authorised user is not an owner of the DM')
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == True:
            valid_message = True         
     #
    if valid_message == False:
        raise error.InputError(description = 'message_id is not a valid message.')
    #    
    is_pinned = True
    if message_id_valid_ch['message_id_valid'] == True:  
        message_index = find_msg_index_ch(message_id)
        if data['messages'][message_index]['is_pinned'] == False:
            is_pinned = False
            data['messages'][message_index]['is_pinned'] = True
    elif message_id_valid_dm['message_id_valid'] == True:
        message_index = find_msg_index_dm(message_id)
        dm_index = select_dm(message_id_valid_dm['dm_id'])
        if data['dms'][dm_index]['messages'][message_index]['is_pinned'] == False:
            is_pinned = False
            data['dms'][dm_index]['messages'][message_index]['is_pinned'] = True
    #               
    if is_pinned == True:
        raise error.InputError(description = f'Message with ID {message_id} is already pinned') 
    save_data(data)    
    return {}  
          
def message_unpin_v1(token, message_id):
    '''
    Given a message_id for a message, pin this message.
    
    Arguments:
        u_id = <class 'int'> - access the user id
        valid_message = <class 'Bool'> - check if the message valid
        message_id_valid_ch = <class 'dict'> check the message is in channel, if it is then return channel id
        message_id_valid_dm = <class 'dict'> check the message is in dm, if it is then return dm id
        is_pinned = <class 'bool'> - check is this message has been unpinned or not


    
    Exceptions:
        AccessError - The authorised user is not a member of the channel or DM that the message is within
        AccessError - The authorised user is not an owner of the channel or DM
        InputError - message_id is not valid
        InputError - message already been unpinned    
    
    Return Value:  
        Returns {}
    '''
    #check token valid
    check_token_valid(token)
    u_id = getUserId(token)
    data = load_data()    
    #
    valid_message = False
    message_id_valid_ch = check_message_id_valid(message_id)
    message_id_valid_dm = check_message_id_valid_all_dm(message_id)
    if message_id_valid_ch['message_id_valid'] == True:
        #
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == False:
            raise error.AccessError(description = 'The authorised user is not a member of the channel that the message is within')
            
        #
        if check_if_user_owner(u_id, message_id_valid_ch['channel_id']) == False:
            raise error.AccessError(description = 'The authorised user is not an owner of the channel')
        #
        if check_member_ch(u_id,message_id_valid_ch['channel_id']) == True:
            valid_message = True
    elif message_id_valid_dm['message_id_valid'] == True:
        #
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == False:
            raise error.AccessError(description = 'The authorised user is not a member of the dm that the message is within')         
        #
        if check_if_user_owner_dm(u_id, message_id_valid_dm['dm_id']) == False:
            raise error.AccessError(description = 'The authorised user is not an owner of the DM')    
        if check_member_dm(u_id,message_id_valid_dm['dm_id']) == True:
            valid_message = True
     #
    if valid_message == False:
        raise error.InputError(description = 'message_id is not a valid message.')
    #    
    is_pinned = False
    if message_id_valid_ch['message_id_valid'] == True:  
         message_index = find_msg_index_ch(message_id)
         if data['messages'][message_index]['is_pinned'] == True:
            is_pinned = True
            data['messages'][message_index]['is_pinned'] = False 
    elif message_id_valid_dm['message_id_valid'] == True:
        message_index = find_msg_index_dm(message_id)
        dm_index = select_dm(message_id_valid_dm['dm_id'])
        if data['dms'][dm_index]['messages'][message_index]['is_pinned'] == True:
            is_pinned = True
            data['dms'][dm_index]['messages'][message_index]['is_pinned'] = False
                   
    if is_pinned == False:
        raise error.InputError(description = f'Message with ID {message_id} is already unpinned')
    save_data(data)
    return {}  
