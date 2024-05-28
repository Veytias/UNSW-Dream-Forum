#from os import O_NOFOLLOW
import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data

'''
Given a User by their user ID, remove the user from the Dreams. 
Dreams owners can remove other **Dreams** owners (including the original first owner). 
Once users are removed from **Dreams**, the contents of the messages they sent will 
be replaced by 'Removed user'. Their profile must still be retrievable with user/profile/v2, 
with their name replaced by 'Removed user'.
'''
def remove(token, u_id):
    '''
    Arguments:
    <OWNER> (<class 'int'>)    - <define OWNER as 1>
    <user_exist> (<class 'bool'>)    - <check given auth_user_id existance>
    <only_owner> (<class 'bool'>)    - <check is there only one owner_user existance>
    ...

    Exceptions:
    InputError  - Occurs when given u_id does not exist
    InputError  - Occurs when there is currently the only owner
    AccessError - Occurs when authorized is not an OWNER or have no permission

    '''
    OWNER = 1 # permision_id 1

    #access database
    data = load_data()
    
    check_token_valid(token)
   

    #check u_id 
    user_exist = False
    for user in range(len(data['users'])):
        if data['users'][user]['u_id'] == u_id:
            user_exist = True

    # InputError  - Occurs when given u_id does not exist
    if user_exist == False:
        raise error.InputError(description=f"Error, {u_id} is not valid")

    auth_id = getUserId(token)
    auth_index = data['users'][auth_id-1]

    # AccessError - Occurs when authorized is not an OWNER or have no permission
    if auth_index['permission_id'] != OWNER:
        raise error.AccessError(description=f"Error, this user doesn't has permission for this action")

    only_owner = False
    count_owner = 0
    for user in range(len(data['users'])):
        if data['users'][user]['permission_id'] == OWNER:
            count_owner += 1

    if count_owner == 1: 
        only_owner = True
        
    # InputError  - Occurs when there is currently the only owner
    if only_owner and auth_id is u_id:
        raise error.InputError(description=f"Error, the user is currently the only owner")

    # replace on meessage which sent by this id with Removed user
    for msg in data['messages']:
        if msg['u_id'] == u_id:
            msg['message'] = 'Removed user'
    
    # remove user from associate channel
    for channel in data['channels']:
        for member in channel['all_members']:
            if u_id == member['u_id']:
                channel['all_members'].remove(member)
    
    # remove user from associate dm
    for dm in data['dms']:
        for member in dm['dm_members']:
            if u_id == member['u_id']:
                dm['dm_members'].remove(member)

    for user in data['users']:
        if user['u_id'] == u_id:
            user['name_first'] = 'Removed user'
            user['name_last'] = 'Removed user'
            user['u_id'] = 'Removed user'
    
    save_data(data)
    return {}

'''
Given a User by their user ID, set their permissions to new permissions described by permission_id
'''
def userpermission(token, u_id, permission_id):
    '''
    Arguments:
    <permission_id_rnage> (<class 'dict'>)    - <range of available permision_ids>
    <user_exist> (<class 'bool'>)    - <check given auth_user_id existance>
    ...

    Exceptions:
    InputError  - Occurs when u_id does not refer to a valid user
    InputError  - Occurs when permission_id does not refer to a value permission
    AccessError - Occurs when authorized is not an OWNER or have no permission

    '''
    # InputError  - Occurs when permission_id does not refer to a value permission
    permission_id_range = {1,2}
    if permission_id not in permission_id_range:
        raise error.InputError(description=f"permission_id does not refer to a value permission")


    #access database
    data = load_data()
    
    check_token_valid(token)

    user_exist = False
    for user in range(len(data['users'])):
        if data['users'][user]['u_id'] == u_id:
            user_exist = True

    # InputError  - Occurs when u_id does not refer to a valid user
    if user_exist == False :
        raise error.InputError(description=f"Error, {u_id} is not valid")

    auth_id = getUserId(token)
    dream_user = data['users'][auth_id-1]
    # AccessError - Occurs when authorized is not an OWNER or have no permission
    if dream_user['permission_id'] != 1:
        raise error.AccessError(description=f"Error, authorised user is not dream user")

    data['users'][u_id-1]['permission_id'] = permission_id
    save_data(data)
    return {}
