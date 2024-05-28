import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data

'''
The list of channels(include details) will be given that the authorize user is a part of.
'''
def channels_list_v2(token):
    # access database
    data = load_data()
    check_token_valid(token)

    u_id =  getUserId(token)

    # Returns <return channels list>
    return {
        'channels': data['users'][u_id-1]['channels']
    }

'''
This will provide the list of all channels that exist and their associated details.
'''
def channels_listall_v2(token):
    # access database
    data = load_data()

    check_token_valid(token)


    all_list = []  # all_list = <class 'list'> -keep dictionary of channels that exist

    for channel in data['channels']:
        channel_index = {'channel_id' : channel['channel_id'], 'name' : channel['name']}
        all_list.append(channel_index.copy())
    
    save_data(data)
    # Returns <return channels list> on <user_exist == True>
    return {
        'channels': all_list
    }

'''
A channel will be created with the given name and given privacy(public or private).
When the channel is created the authorise user will be the owner and first member of the created channel.
The user information on the channels that they are a member of will also be updated.
'''
def channels_create_v2(token, name, is_public):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    <name_length> <class 'int'> <check given channel_name is longer than 20 or not
    <new_member> <class 'dict'> <contain the information of the user who create the channel>
    ...

    Exceptions:
    InputError  - Occurs when given channel_name is longer than 20 characters

    Return Value:
    Returns <return dict(channel_id)> on <name_length <= 20>    '''
    data = load_data()    
    check_token_valid(token)    
    u_id = getUserId(token)
    # check channel_name is longer than 20 or not.
    name_length = len(name)  # name_length = <class 'str'> -length of the given name
    # InputError -Occur when the given name is more than 20 characters
    if name_length > 20:
        raise error.InputError(description= 'Name is more than 20 characters long')
        
    # generate channel id
    channel_id = len(data['channels'])+1
    new_member = None 

    # creater join channel's members and onwers list
    for user in data['users']:
        if u_id == user['u_id']:
            new_member = {'u_id':user['u_id'],'name_first':user['name_first'],'name_last':user['name_last'],'email':user['email'],'handle_str':user['handle_str'], 'profile_img_url': user['profile_img_url']}
    #add channel information into related database
    data['channels'].append({'channel_id': channel_id,   
                             'name':name,   
                             'owner_members':[new_member],
                             'all_members':[new_member],
                             'is_public': is_public})
    data['users'][u_id-1]['channels'].append({'channel_id': channel_id,   
                             'name':name})
    save_data(data)                         
    # Returns <return dict(channel_id)> on <name_length <= 20>                         
    return {
        'channel_id': channel_id,
    }
