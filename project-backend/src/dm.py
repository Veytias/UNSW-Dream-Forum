import src.error as error 
from src.helper import getUserId,check_token_valid,load_data,save_data

'''
Helper functions
'''

def select_dm(dm_id):
    data = load_data()
    BEGIN = 0
    dm_order = BEGIN
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return dm_order
        dm_order += 1
    return False


def notification_invite_dm(auth_id, u_id, dm_id):
    data = load_data()
    auth_handle = data['users'][auth_id -1]['handle_str']
    dm_index = select_dm(dm_id)
    dm_name = data['dms'][dm_index-1]['dm_name']    
    noti_message = f"{auth_handle} added you to {dm_name}"
    data['users'][u_id - 1]['notifications'].append({'channel_id': -1, 'dm_id': dm_id, 'notification_message':noti_message})
    save_data(data)
   
'''
Invite a person to a dm with valid token and u_id
'''
def dm_invite_v1(token, dm_id, u_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_exist> - <class 'bool'> - <check given dm_id existance>
    <user_exist> -  <class 'bool'> - <check u_id existance>
    <auth_user> -  <class 'bool'> - <check auth_id not member of dm>
    ...

    Exceptions:
    InputError  - Occurs when the given dm_id does not exist
                - Occurs when the given u_id does not exist 
    AccessError - Occurs when the autorized user(inviter) is not already a member of the dm  

    Return Value:
    Returns <return dict({})> on <dm_exist == True && auth_user == True && user_owner == True>
    '''
    dm_exist = False
    user_exist = False
    auth_user = False
    user_index = 'empty'

    data = load_data()    
    check_token_valid(token)

    auth_id = getUserId(token)

    dm_index = select_dm(dm_id)
    if dm_index is not False:
        dm_exist = True
       
    # InputError - Occurs when the given dm_id does not exist
    if dm_exist == False:
        raise error.InputError(description= "Error, {dm_id} is not valid")

    for user in data['users']:
        if user['u_id'] == u_id:
            user_exist = True
            user_index = data['users'][u_id-1]
    # InputError - Occurs when the given u_id does not exist      
    if user_exist == False :
        raise error.InputError(description= "Error, {u_id} is not valid")   

    for member in data['dms'][dm_index]['dm_members']:
        if member['u_id'] == auth_id:
            auth_user = True
            new_user = {'u_id': u_id, 'name_first': user_index['name_first'], 'name_last': user_index['name_last'], 'email': user_index['email'], 'handle_str': user_index['handle_str'], 'profile_img_url': user_index['profile_img_url']}
            data['dms'][dm_index]['dm_members'].append(new_user.copy())
            save_data(data)
            notification_invite_dm(auth_id, u_id, dm_id)
            data = load_data()

    # AccessError - Occurs when the autorized user(inviter) is not already a member of the dm           
    if auth_user == False:
        raise error.AccessError(description= "Error, {auth_id} is not member of the dm")

    save_data(data)


    return {
    }

'''
remove a dm with given dm_id from the database.
'''
def dm_remove_v1(token, dm_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_exist> - <class 'bool'> - <check given dm_id existance>
    <auth_user_owner> -  <class 'bool'> - <check auth_id is owner of dm>
    ...

    Exceptions:
    InputError  - Occurs when the given dm_id does not exist
                
    AccessError - Occurs when the autorized user is not owner of the dm 

    Return Value:
    Returns <return dict({})> on <dm_exist == True && auth_user_owner == True>
    '''
    dm_exist = False
    auth_user_owner = False

    data = load_data()    
    check_token_valid(token)
    
    auth_id = getUserId(token)

    dm_index = select_dm(dm_id)
    if dm_index is not False:
        dm_exist = True
       
    # InputError - Occurs when the given dm_id does not exist
    if dm_exist == False:
        raise error.InputError(description= "Error, {dm_id} is not valid")
    
    if data['dms'][dm_index]['dm_owner'] == auth_id:
        auth_user_owner = True
        data['dms'].pop(dm_index)
       

    # AccessError - Occurs when the autorized user is not owner of the dm       
    if auth_user_owner == False:
        raise error.AccessError(description= "Error, {auth_id} is not owner of the dm") 

    save_data(data)

    return {
    }
'''
A dm will be created with the given u_ids.
When the dm is created the authorise user will be the owner and member of the created channel.
'''
def dm_create_v1(token, u_ids):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <valid_user> <class 'bool'> <check given user is vaild or not>
    <dm_name> <class 'list'> <used for store the handle of users for dm_name>
    <dm_members> <class 'list'> <used for store the members of dm>
    <member_dict> <class 'dict'> <used for store the members's information>
    Exceptions:
    InputError  - Occurs when the given u_ids does not exist    

    Return Value:
    Returns <return dict(dm_id,dm_name)> on <valid_user != False>  
    '''
    data = load_data()   
    #check token is valid or not
    check_token_valid(token)
    auth_id = getUserId(token)
    #check u_id in u_ids is vaild or not
    for u_id in u_ids:
        valid_user = False
        for user in data['users']:
            if user['u_id'] == u_id:
                valid_user = True
    #InputError - Occurs when the given u_ids does not exist            
    if valid_user == False:
        raise error.InputError(description= "u_id does not refer to a valid user")
    dm_name = []
    dm_members = []
    dm_id = len(data['dms'])+1
    #add auth_user into dm
    handle = data['users'][auth_id-1]['handle_str']
    name_first = data['users'][auth_id-1]['name_first']
    name_last = data['users'][auth_id-1]['name_last']
    email = data['users'][auth_id-1]['email']
    profile_img_url = data['users'][auth_id-1]['profile_img_url']
    member_dict = {'u_id':auth_id,
                       'name_first':name_first,
                       'name_last':name_last,
                       'email':email,
                       'handle_str':handle,
                       'profile_img_url': profile_img_url}
    dm_name.append(handle)
    dm_members.append(member_dict)
    #add u_ids into dm
    for u_id in u_ids:
        handle = data['users'][u_id-1]['handle_str']
        name_first = data['users'][u_id-1]['name_first']
        name_last = data['users'][u_id-1]['name_last']
        email = data['users'][u_id-1]['email']
        profile_img_url = data['users'][auth_id-1]['profile_img_url']
        member_dict = {'u_id':u_id,
                       'name_first':name_first,
                       'name_last':name_last,
                       'email':email,
                       'handle_str':handle,
                       'profile_img_url': profile_img_url}
        dm_name.append(handle)
        dm_members.append(member_dict)
        
    #sort dm_name alphabetically
    dm_name = sorted(dm_name)
    dm_name = ', '.join(dm_name)
    dm_owenr = auth_id
    messages = []
    #create dm information
    data['dms'].append({'dm_id':dm_id,
                        'dm_name':dm_name,
                        'dm_owner':dm_owenr,
                        'dm_members':dm_members,
                        'messages':messages})              
    save_data(data)
    for u_id in u_ids:   
        notification_invite_dm(auth_id, u_id, dm_id)
        data = load_data()
        save_data(data)                                           
    return {
        'dm_id': dm_id,
        'dm_name': dm_name
    }
    
'''
The authorised user will be delete from the given dm.
'''    
def dm_leave_v1(token, dm_id):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_validity>  <class 'bool'> - <check given dm_id existance>
    <access>  <class 'bool'> - <check given authorize user is can visit this dm or not>
    Exceptions:
    InputError  - Occurs when given dm_id does not exist
    AccessError - Occurs when authorized user is not a member of the given dm_id

    Return Value:
    Returns <return dict({})> on <dm_validity == True && access == True>
    '''
    data = load_data()    
    #check token is valid or not
    check_token_valid(token)
    dm_validity = False # dm_validity = <class 'bool'> -check given dm_id existance
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            dm_validity = True
    # check dm validity
    # InputError - Occurs when the given dm_id does not exist   
    if dm_validity == False:
        raise error.InputError(description= f'dm_id [{dm_id}] is not a valid DM')
     # check auth user has access to visit this dm
    access = False  # access = <class 'bool'> - check given authorize user is can visit this dm or not
    u_id = getUserId(token)
    #user = data['users'][u_id - 1]
    dm = data['dms'][dm_id-1]
    for member in dm['dm_members']:
        if u_id == member['u_id']:
            access = True
    # AccessError - Occurs when authorized user is not a member of the given dm_id
    if access == False:
        raise error.AccessError(description= f"Authorised user [{u_id}] is not a member of DM with dm_id[{dm_id}]") 
    for member in dm['dm_members']:
        if u_id == member['u_id']:
            dm['dm_members'].remove(member)
    save_data(data)       
    return {}
    
'''
this function will read up to 50 most recent direct messages from start position in DM [dm_id].
''' 
def dm_messages_v1(token, dm_id, start):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <dm_validity>  <class 'bool'> - <check given dm_id existance>
    <dm_number> <class 'int'> - <check the total number of messages in this dm>
    <access> <class 'bool'> - <check given authorize user is can visit this dm or not>

    Exceptions:
    InputError  - Occurs when given dm_id does not exist
                - Occurs when message start position is greater 
                  than the total number of direct messages in the dm
    AccessError - Occurs when authorized user is not a member of the given dm_id

    Return Value:
    Returns Returns <return dict(message_list, start, end) > on <access == True and dm_validity == True and start > dm_number>
    '''
    data = load_data()    
    check_token_valid(token)
    u_id = getUserId(token)
    dm_validity = False  # dm_validity = <class 'bool'> - check given dm_id existance
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            dm_validity = True
    # check dm validity
    # InputError - Occurs when given dm_id does not exist
    if dm_validity == False:
        raise error.InputError(description= f'DM ID [{dm_id}] is not a valid DM')
        
    dm = data['dms'][dm_id-1]
    # check start is greater than the total number of messages in the dm
    dm_number = len(dm['messages'])
    # InpurError - Occurs when message start position is greater than the total number of messages in the dm
    if start  > dm_number:
        raise error.InputError(description= f"start is greater than the total number of messages in the DM")

    # check auth user has access to visit this dm
    access = False  # access = <class 'bool'> - check given authorize user is can visit thish dm or not
    
    for member in dm['dm_members']:
        if u_id == member['u_id']:
            access = True

    # AccessError - Occurs when authorized user is not a member of the given dm_id
    if access == False:
        raise error.AccessError(description= f"Authorised user [{u_id}] is not a member of DM with dm_id[{dm_id}]")
    # read messages of this dm
    end = start + 50  
    counter = 0
    messages_list = []  # messages_list = <classs 'list'> - used for storing every message that meet the conditions
    for message in dm['messages']:
        if counter <= end:
            messages_list.append(message)
            counter += 1
    # check if it has more message to read
    if end > dm_number:
        end = -1
       
    return {
        'messages': messages_list,'start': start,'end': end,
    }


'''
Users that are part of this direct message can view basic 
information about the DM
'''
def dm_details_v1(token, dm_id):
    '''
    Arguments:
    <dm_exist> (<class 'bool'>)    - <check dm existance>
    <user_access> (<class 'bool'>)    - <check given auth_user_id existance>
    <dm_index> (<class 'int'>)    - <user as selected dm from list>

    Exceptions:
    InputError  - Occurs when given dm_id does not exist
    AccessError - Occurs when authorized user is not a member of the given dm_id

    Return Value:
    Returns <return dict(name, members)> on <user_access == True && dm_id is exist>
    '''
    
	#access database
    data = load_data()
    
    check_token_valid(token)
    
    dm_exist = False
    dm_index = select_dm(dm_id)
    if dm_index is not False:
        dm_exist = True
       
    # InputError - Occurs when the given dm_id does not exist
    if dm_exist == False:
        raise error.InputError(description= "Error, {dm_id} is not valid")

    u_id = getUserId(token)
    user_access = False
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            for member in dm['dm_members']:
                if u_id == member['u_id']:
                    user_access = True

    # AccessError - Occurs when authorized user is not a member of the given channel_id
    if user_access == False:
        raise error.AccessError(description= "Authorised user is not part of dm")

    res_dm = data['dms'][dm_index]
    
    return {
    	'name' : res_dm['dm_name'],
    	'members' : res_dm['dm_members']
    }

'''
Returns the list of DMs that the user is a member of
'''
def dm_list_v1(token):
    #access database
    data = load_data()
    
    check_token_valid(token)
    
    u_id = getUserId(token)
        
    dm_list = []
    for dm in range(len(data['dms'])):
        dm_id = data['dms'][dm]['dm_id']
        dm_name = data['dms'][dm]['dm_name']
        for member in range(len(data['dms'][dm]['dm_members'])):
            members = data['dms'][dm]['dm_members'][member]
            if members['u_id'] == u_id:
                dm_list.append({'dm_id':dm_id,'name':dm_name})
                continue
    return {
        'dms' : dm_list
    }

