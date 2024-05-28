import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data

SECRET = "Sunshine"


'''
help function
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

def notification_invite_ch(auth_id, u_id, channel_id):
    data = load_data()
    auth_handle = data['users'][auth_id -1]['handle_str']
    ch_index = select_channel(channel_id)
    channel_name = data['channels'][ch_index]['name']    
    noti_message = f"{auth_handle} added you to {channel_name}"
    data['users'][u_id - 1]['notifications'].append({'channel_id': channel_id, 'dm_id': -1, 'notification_message':noti_message})
    save_data(data)
    
'''
The authorize user id is the inviter and authorize u_id will be the one who got invite to the target channel_id.
'''
def channel_invite_v2(token, channel_id, u_id):
    '''
    Arguments:
    <channel_exist>  <class 'bool'>  -check given channel_id existance
    <user_exist>  <class 'bool'>   -check given u_id existance
    <auth_user>  <class 'bool'>	  -check given auth_user_id existance
    <invitee>  <class 'str'>	    -access invitee id in database(will be change to int)
    <channel_name>  <class 'str'>  -keep channel name of the channel_id
    <channel_index>  <class 'int'>   -index of the given channel in list of channelst>
    ...

    Exceptions:
    InputError  - Occurs when the given u_id does not exist 
            - Occurs when the given channel_id does not exist
    AccessError - Occurs when the authorized user(inviter) is not already a member of the channel

    Return Value:
    Returns <return dict({})> on <channel_exist == True && user_exist == True && auth_user == True>
    '''
    channel_exist = False   
    user_exist = False      
    auth_user = False       
    invitee = 'dict'        
    channel_name = 'name'   
    channel_index = 0      
    
    check_token_valid(token)
    
        
    data = load_data()

    # uid does not refer to a valid user
    for user in range(len(data['users'])):
        if data['users'][user]['u_id'] == u_id:
            user_exist = True
            invitee = data['users'][user]

    # InputError - Occurs when the given u_id does not exist      
    if user_exist == False :
        raise error.InputError(description= "Error, {u_id} is not valid")   
            	
    # check whether the input channel exist or not    
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True
        channel_name = data['channels'][channel_index]['name']
            
    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False :
        raise error.InputError(description= "Error, {channel_id} is not valid") 

    user_id = getUserId(token) 

    for member in range(len(data['channels'][channel_index]['all_members'])):
        # check authorised user is not already a member of the channel
        if data['channels'][channel_index]['all_members'][member]['u_id'] == user_id :
            auth_user = True

            # add new user as a member in channels
            new_user = {'u_id': u_id, 'name_first': invitee['name_first'], 'name_last': invitee['name_last'], 'email': invitee['email'], 'handle_str': invitee['handle_str'], 'profile_img_url': invitee['profile_img_url']}
            data['channels'][channel_index]['all_members'].append(new_user.copy())

            # add channel_id and channel_name in users
            add_channel = {'channel_id' : channel_id, 'name' : channel_name}
            invitee['channels'].append(add_channel.copy())
            save_data(data)
            notification_invite_ch(user_id, u_id, channel_id)
            data = load_data()

    # AccessError - Occurs when the authorized user(inviter) is not already a member of the channel           
    if auth_user == False :
        raise error.AccessError(description= "The given token is not valid") 

    save_data(data)
                     
    return {
    }

'''
The details of the channel will that the authorize user id is a member of will
be given, which include name, owner members, and all members.
'''
def channel_details_v2(token, channel_id):
    '''
    Arguments:
    <channel_selected_id> (<class 'bool'>)    - <check  channel_id existance>
    <user_access> (<class 'bool'>)    - <check given auth_user_id existance>
    <channel_selected_index> (<class 'int'>)    - <user as selected channel from list>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    AccessError - Occurs when authorized user is not a member of the given channel_id

    Return Value:
    Returns <return dict(name, owner_member,all_member)> on <user_access == True && channel_selected_id is exist>
    '''
    # access database
    data = load_data()

    check_token_valid(token)

    u_id =  getUserId(token)

    # find if channel_id exist
    # channel_selected_id = <class 'int'> -check given channel_id existance
    channel_selected_id = select_channel(channel_id)  

    # InputError - Occurs when given channel_id does not exist 
    if channel_selected_id is False:
        raise error.InputError(description= 'Error: selected channel is invalid.')  

    # channel_selected_index = <class 'int'> -index of the given channel in list of channels
    channel_selected_index = data['channels'][channel_selected_id] 

    # find if u_id is part of the selected channel
    # access = <class 'bool'> - check given u_id existance
    user_access = False
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            for member in channel['all_members']:
                if u_id == member['u_id']:
                    user_access = True

    # AccessError - Occurs when authorized user is not a member of the given channel_id
    if user_access == False:
        raise error.AccessError(description= "Authorised user [{u_id}] is not a member of channel with channel id[{channel_id}]")

    # Returns <return dict(name, owner_member,all_member) > on <access == True and channel_selected_id > len(data['channels']>
    return {
        'name' : channel_selected_index['name'],
        'is_public' : channel_selected_index['is_public'],
        'owner_members' : channel_selected_index['owner_members'],
        'all_members' : channel_selected_index['all_members'],
    }


    

'''
this function will read up to 50 most recent messages from start position in channel [channel_id].
'''
def channel_messages_v2(token, channel_id, start):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_validity>  <class 'bool'> - <check given channel_id existance>
    <messages_number> <class 'int'> - <check the total number of messages in this channel>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
                - Occurs when message start position is greater 
                  than the total number of messages in the channel
    AccessError - Occurs when authorized user is not a member of the given channel_id

    Return Value:
    Returns <return dict(messages, start,end)> on <channel_validity == True && start is greater than end && given token is the member of this channel>'''
    data = load_data()    
    check_token_valid(token)
    u_id = getUserId(token)
    channel_validity = False  
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel_validity = True
    # check channel validity
    if channel_validity == False:
        raise error.InputError(description=f'Channel ID [{channel_id}] is not a valid channel')

    # check start is greater than the total number of messages in the channel
    messages_number = 0  # 
    for message in data['messages']:
        if channel_id == message['channel_id']:
            messages_number += 1

    # InpurError - Occurs when message start position is greater than the total number of messages in the channel
    if start > messages_number:
        raise error.InputError(description = "start is greater than the total number of messages in the channel")

    # check auth user has access to visit this channel
    access = False  # access = <class 'bool'> - check given authorize user is can visit thish channel or not
    channel = data['channels'][channel_id-1]
    for member in channel['all_members']:
        if u_id == member['u_id']:
            access = True

    # AccessError - Occurs when authorized user is not a member of the given channel_id
    if access == False:
        raise error.AccessError(description=f"Authorised user [{u_id}] is not a member of channel with channel id[{channel_id}]")
    # read messages of this channel
    # end = <class 'int'> - store the end position of messages that has been read(start + 50),but be -1 when there are no more messages to read.
    end = start + 50  
    messages_read = 0
    messages_list = []  # messages_list = <classs 'list'> - used for storing every message that meet the conditions
    for message in data['messages']:
        if channel_id == message['channel_id'] and messages_read < end:
            messages_list.append(message)
            messages_read += 1
    # check if it has more message to read
    if end > messages_number:
        end = -1
       
    # Returns <return dict(message_list, start, end) > on <access == True and channel_validity == True and start > message_number>
    return {
        'messages': messages_list,'start': start,'end': end,
    }
'''
The authorised user will be delete from the given channel id.
'''
def channel_leave_v1(token, channel_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_validity>  <class 'bool'> - <check given channel_id existance>
    <access>  <class 'bool'> - <check given authorize user is can visit thish channel or not>

    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    AccessError - Occurs when authorized user is not a member of the given channel_id

    Return Value:
    Returns <return dict({})> on <channel_validity == True && access == True>'''
    data = load_data()    
    check_token_valid(token)
    u_id = getUserId(token)
    channel_validity = False # channel_validity = <class 'bool'> -check given channel_id existance
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel_validity = True
    # check channel validity
    # InputError - Occurs when the given channel_id does not exist   
    if channel_validity == False:
        raise error.InputError(description=f'Channel ID [{channel_id}] is not a valid channel')
    # check auth user has access to visit this channel
    access = False  
    channel = data['channels'][channel_id-1]
    for member in channel['all_members']:
        if u_id == member['u_id']:
            access = True
    # AccessError - Occurs when authorized user is not a member of the given channel_id
    if access == False:
        raise error.AccessError(description=f"Authorised user [{u_id}] is not a member of channel with channel id[{channel_id}]")
    #delete user's information of given channel
    for member in data['channels'][channel_id - 1]['all_members']:
        if u_id == member['u_id']:
            data['channels'][channel_id-1]['all_members'].remove(member)
    #delete channel information of given user's joined channels list
    for channel in data['users'][u_id - 1]['channels']:
        if channel_id == channel['channel_id']:
            data['users'][u_id - 1]['channels'].remove(channel)
    save_data(data)
    #return empty dict
    return {
    }
'''
The authorised user id will be added to the given channel id.
'''
def channel_join_v2(token, channel_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_validity>  <class 'bool'> - <check given channel_id existance>
    <permission_id>  <class 'int'> - <check given authorize user have permission to 
                                        add private channel>

    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
    AccessError - Occurs when the given channel is private

    Return Value:
    Returns <return dict({})> on <channel_validity == True && have permission to join given channel>'''
    data = load_data()    
    check_token_valid(token)
    u_id = getUserId(token)
    channel_validity = False # channel_validity = <class 'bool'> -check given channel_id existance
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel_validity = True
    # check channel validity
    # InputError - Occurs when the given channel_id does not exist
    
    if channel_validity == False:
        raise error.InputError(description=f'Channel ID [{channel_id}] is not a valid channel')
    # check channel is private or not
    channel = data['channels'][channel_id-1]

    # AccessError - Occurs when the given channel is private
    permission_id = data['users'][u_id-1]['permission_id']
    if channel['is_public'] == False and permission_id != 1:
        raise error.AccessError(description=f'channel_id [{channel_id}]refers to a channel that is private')

    # join auth_user into channel
    user = data['users'][u_id-1]
    channel['all_members'].append({'u_id':user['u_id'],
                                   'email':user['email'],
                                   'name_first':user['name_first'],
                                   'name_last':user['name_last'],
                                   'handle_str':user['handle_str'],
                                   'profile_img_url': user['profile_img_url']})
    channel['owner_members'].append({'u_id':user['u_id'],
                                   'email':user['email'],
                                   'name_first':user['name_first'],
                                   'name_last':user['name_last'],
                                   'handle_str':user['handle_str'],
                                   'profile_img_url': user['profile_img_url']})                                 
    user['channels'].append({'channel_id':channel['channel_id'],
                             'name':channel['name']})      
    
    save_data(data)
    #return empty dict       
    return {
    }

'''
add owner to the given channel(assume the u_id is already member of the channel)
'''
def channel_addowner_v1(token, channel_id, u_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_exist> - <class 'bool'> - <check given channel_id existance>
    <uid_owner> -  <class 'bool'> - <check u_id owner>
    <auth_owner> -  <class 'bool'> - <check auth_id owner>
    ...
    Exceptions:
    InputError  - Occurs when given channel_id does not exist
                - Occurs when u_id is an owner of the channel
    AccessError - Occurs when auth_id is not an owner of the channel

    Return Value:
    Returns <return dict({})> on <channel_exist == True && auth_owner == True && uid_owner == False>
    '''
    channel_exist = False
    uid_owner = False
    auth_owner = False
    channel = 'dict'

    check_token_valid(token)
    
    data = load_data()
    auth_id = getUserId(token)

    # check whether the input channel exist or not    
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True
        channel = data['channels'][channel_index]

    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    # check if u_id and auth_id is an owner
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            uid_owner = True

        if owner['u_id'] == auth_id:
            auth_owner = True
    
    # InputError - Occurs when u_id is an owner of the channel
    if uid_owner == True:
        raise error.InputError(description= "Error, {u_id} is already an owner of this channel")

    # AccessError - Occurs when auth_id is not an owner of the channel
    if auth_owner == False and auth_id != 1:
        raise error.AccessError(description= "authorized user is not an owner of this channel")

    if u_id is not None:
        owner_det = data['users'][u_id-1]
    else:
        raise error.InputError(description= "Error, u_id is None")

    new_owner = {'u_id': u_id, 'name_first': owner_det['name_first'], 'name_last': owner_det['name_last'], 'email' : owner_det['email'], 'handle_str': owner_det['handle_str'], 'profile_img_url': owner_det['profile_img_url']} 
    channel['owner_members'].append(new_owner.copy())
    
    save_data(data)
    notification_invite_ch(auth_id, u_id, channel_id)
    data = load_data()
    save_data(data)
    return {
    }

'''
remove owner with given u_id from specified channel
'''
def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <channel_exist> - <class 'bool'> - <check given channel_id existance>
    <uid_owner> -  <class 'bool'> - <check u_id owner>
    <auth_owner> -  <class 'bool'> - <check auth_id owner>
    ...

    Exceptions:
    InputError  - Occurs when given channel_id does not exist
                - Occurs when u_id is not an owner of the channel
                - Occurs when there's only one owner
    AccessError - Occurs when auth_id is not an owner of the channel

    Return Value:
    Returns <return dict({})> on <channel_exist == True && auth_owner == True && uid_owner == True>
    '''
    channel_exist = False
    uid_owner = False
    auth_owner = False
    owner_index = 0
    channel = 'dict'

    check_token_valid(token)

    data = load_data()
    auth_id = getUserId(token)

    # check whether the input channel exist or not    
    channel_index = select_channel(channel_id)
    if channel_index is not False:
        channel_exist = True
        channel = data['channels'][channel_index]

    # InputError - Occurs when the given channel_id does not exist
    if channel_exist == False:
        raise error.InputError(description= "Error, {channel_id} is not valid")

    # check if u_id and auth_id is an owner
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            uid_owner = True

        if owner['u_id'] == auth_id:
            auth_owner = True
    
    # InputError - Occurs when u_id is not an owner of the channel
    if uid_owner == False:
        raise error.InputError(description= "Error, {u_id} not an owner of this channel")

    # AccessError - Occurs when auth_id is not an owner of the channel
    if auth_owner == False and auth_id != 1:
        raise error.AccessError(description= "authorized user is not an owner of this channel")

    # InpurError - Occurs when there's only one owner
    if len(channel['owner_members']) == 1:
        raise error.InputError(description= "This user is currently the only owner in this channel")
    print(channel['owner_members'])
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            break
        owner_index+=1

    channel['owner_members'].pop(owner_index)
    print(channel['owner_members'])
    save_data(data)


    return {
    }
