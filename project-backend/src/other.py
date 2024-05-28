from src.helper import getUserId,check_token_valid,load_data,save_data
import src.error as error
from datetime import datetime
import re

def clear_v1():
    data = load_data()   
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()
    data['dms'].clear()
    data['standups'].clear()
    data['dreams_stats']['channels_exist'].clear()
    data['dreams_stats']['dms_exist'].clear()
    data['dreams_stats']['messages_exist'].clear()
    save_data(data)
    return {}

'''
Given a query string, return messages that match the string as a list
'''
def search_v2(token,query_str):
    '''
    Arguments:
    <data> (class 'dict') - <all information where read from database.p>
    ...

    Exceptions:
                 
    InputError - Occurs when query_str is above 1000 characters

    Return Value:
    Returns <return dict(search_result)> on <query_str <= 1000>
    '''

    search_result = []

    check_token_valid(token)

    #raise inputError
    if len(query_str) > 1000:
        raise error.InputError(description="Message should be no more than 1000 characters")

    if query_str == '':
        return {'messages': []}
    
    data = load_data()
    auth_user = getUserId(token)

    for user_ch in data['users'][auth_user-1]['channels']:
        for messages in data['messages']:
            if user_ch['channel_id'] == messages['channel_id']:
                if re.search(str(query_str), messages['message']):
                    search_result.append(messages['message'])

    for dm in data['dms']:
        for member in dm['dm_members']:
            if member['u_id'] == auth_user:
                for messages in dm['messages']:
                    if re.search(str(query_str), messages['message']):
                        search_result.append(messages['message'])
                
    return {'messages': search_result}

