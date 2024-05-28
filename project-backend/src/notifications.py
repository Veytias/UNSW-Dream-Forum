import src.error as error
from src.helper import getUserId,check_token_valid,load_data,save_data

'''
this function will read up to 20 most recent notifications for given user.
'''
def notifications_get_v1(token):
    '''
    Arguments:
        <data> (class 'dict') - <all information where read from database.p>
        <notifications> (class 'dict') - <store up to 20 notifications of given users>

    Return Value:
        Returns <return dict(notifications)>'''


    data = load_data()    
    #check token is valid or not
    check_token_valid(token)
    u_id = getUserId(token)
    notifications = data['users'][u_id-1]['notifications']      
    notifications = notifications[:20]
    return { 'notifications':notifications }
