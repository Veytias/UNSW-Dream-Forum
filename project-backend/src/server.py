#import sys

from json import dumps
from flask import Flask, request, send_from_directory, abort
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2 as login
from src.auth import auth_register_v2 as register
from src.auth import auth_logout_v1 as logout
from src.auth import auth_passwordreset_request_v1 as request_reset
from src.auth import auth_passwordreset_reset_v1 as reset_password
from src.channels import channels_create_v2 as create_channel
from src.channels import channels_list_v2 as list_channel
from src.channels import channels_listall_v2 as listall_channel
from src.channel import channel_details_v2 as details_channel
from src.channel import channel_messages_v2 as read_channel_messages
from src.channel import channel_join_v2 as join_channel
from src.channel import channel_leave_v1 as leave_channel
from src.channel import channel_invite_v2 as invite_channel
from src.channel import channel_addowner_v1 as addowner_channel
from src.channel import channel_removeowner_v1 as removeowner_channel
from src.dm import dm_create_v1 as create_dm
from src.dm import dm_leave_v1 as leave_dm
from src.dm import dm_messages_v1 as read_dm
from src.dm import dm_list_v1 as list_dm
from src.dm import dm_invite_v1 as invite_dm
from src.dm import dm_remove_v1 as remove_dm
from src.dm import dm_details_v1 as details_dm
from src.user import user_profile_v2 as user_profile
from src.user import user_profile_setname_v2 as user_profile_setname
from src.user import user_profile_setemail_v2 as user_profile_setemail
from src.user import user_profile_sethandle_v1 as user_profile_sethandle
from src.user import users_all_v1 as users_all
from src.user import user_profile_uploadphoto_v1 as user_profile_uploadphoto
from src.user import user_stats_v1 as user_stats
from src.user import users_stats_v1 as users_stats
from src.message import message_send_v2 as send_message
from src.message import message_remove_v1 as remove_message
from src.message import message_edit_v2 as edit_message
from src.message import message_senddm_v1 as send_dm
from src.message import message_share_v1 as share_message
from src.message import message_sendlater_v1 as sendlater_message
from src.message import message_sendlaterdm_v1 as sendlaterdm_message
from src.message import message_react_v1 as message_react
from src.message import message_unreact_v1 as message_unreact
from src.message import message_pin_v1 as message_pin
from src.message import message_unpin_v1 as message_unpin
from src.notifications import notifications_get_v1 as read_notifications
from src.other import search_v2
from src.admin import remove, userpermission
from src.helper import load_data
from flask_mail import Mail, Message
from src.standup import standup_start, standup_active, standup_send

#from src.helper import load_data
from src.other import clear_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'joannayinyuemeng@gmail.com',
	MAIL_PASSWORD = '123??abc!'
	)

CORS(APP)


#function for sending reset code
def send_email_reset(email, content):
   mail = Mail(APP)
   #send email with reset code
   msg = Message("reseting password", sender = 'sender@gmail.com', recipients = [email])
   msg.body = f"You or someone else has requested that a new password be generated for your account. Use reset_code: {content}."
   mail.send(msg)
   return 

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
    

@APP.route("/")
def hello():
    return "Hello"
 
'''
auth routes
'''


@APP.route("/auth/login/v2", methods=['POST'])
def connect():
    '''
    user connect to server through email and password,
    return token and u_id
    '''
    
    auth = request.get_json()
    
    ret = login(auth['email'], auth['password'])
    return dumps(ret)
    
@APP.route("/auth/register/v2", methods=['POST'])
def create_auth():
    '''
    user create account by inputing email,password,firstname,lastname,
    return token and u_id
    '''
    auth = request.get_json()
    
    ret = register(auth['email'], 
                   auth['password'],
                   auth['name_first'], 
                   auth['name_last'])
    return dumps(ret)

@APP.route("/auth/logout/v1", methods=['POST'])
def disconnect():
    '''
    user disconnect fromthe server by checking token
    return "is_success" True or False
    '''
    auth = request.get_json()
    
    ret = logout(auth['token'])
    return dumps(ret)

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def reset_pass_request():
    '''
    user request reset password
    '''
    auth = request.get_json()
    email = auth['email']
    data = load_data()
    request_reset(email)
    
    for user in data['users']:
        if email == user['email']:
            reset_code = user['reset_code']
            send_email_reset(email, reset_code)
	
    return dumps({})

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def reset_pass_reset():
    '''
    user request reset password
    '''
    auth = request.get_json()
    reset_password(auth['reset_code'], auth['new_password'])
    return dumps({})
'''
channel routes
'''
@APP.route('/channel/details/v2', methods=['GET'])
def channel_detail():
    
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    details = details_channel(token, int(channel_id))
    return dumps(details)
    

@APP.route('/channel/messages/v2', methods=['GET'])
def channel_messages():
    
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    messages = read_channel_messages(token,int(channel_id),int(start))
    return dumps(messages)
    
@APP.route('/channel/join/v2', methods=['POST']) 
def join_ch():
    channel_info = request.get_json()
    token = channel_info['token']
    channel_id = channel_info['channel_id']
    result = join_channel(token,channel_id)
    return dumps(result)
    
@APP.route('/channel/leave/v1', methods=['POST'])
def leave_ch():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    result = leave_channel(token,channel_id)
    return dumps(result)

@APP.route('/channel/invite/v2', methods=['POST'])
def invite_ch():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    u_id = args['u_id']
    invite_channel(token, channel_id, u_id)
    return dumps({})

@APP.route('/channel/addowner/v1', methods=['POST'])
def addowner_ch():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    u_id = args['u_id']
    addowner_channel(token, channel_id, u_id)
    return dumps({})

@APP.route('/channel/removeowner/v1', methods=['POST'])
def removeowner_ch():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    u_id = args['u_id']
    removeowner_channel(token, channel_id, u_id)
    return dumps({})


'''
channels routes
'''
@APP.route('/channels/create/v2', methods=['POST'])
def create_ch():
    args = request.get_json()
    token = args['token']
    name = args['name']
    is_public = args['is_public']
    channel = create_channel(token,name,is_public)
    return dumps(channel)
    
@APP.route('/channels/list/v2', methods=['GET'])
def list_ch():
    
    token = request.args.get('token')
    channel = list_channel(token)
    return dumps(channel)

@APP.route('/channels/listall/v2', methods=['GET'])
def listall_ch():
    
    token = request.args.get('token')
    channel = listall_channel(token)
    return dumps(channel)
'''
dm routes
'''
@APP.route('/dm/details/v1', methods=['GET'])
def dm_details():
    
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    details = details_dm(token, int(dm_id))
    return dumps(details)

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create():
    args = request.get_json()
    token = args['token']
    u_ids = args['u_ids']
    dm = create_dm(token,u_ids)
    return dumps(dm)
@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    args = request.get_json()
    token = args['token']
    dm_id = args['dm_id']
    result = leave_dm(token,int(dm_id))
    return dumps(result)
@APP.route('/dm/messages/v1', methods=['GET'])
def dm_read():
    
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    messages = read_dm(token, int(dm_id), int(start))  
    return dumps(messages)
@APP.route('/dm/list/v1', methods=['GET'])
def dm_list():
    
    token = request.args.get('token')
    dm_list = list_dm(token)  
    return dumps(dm_list)   

@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite():
    args = request.get_json()
    token = args['token']
    dm_id = args['dm_id']
    u_id = args['u_id']
    invite_dm(token, dm_id, u_id)
    return dumps({})

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove():
    args = request.get_json()
    token = args['token']
    dm_id = args['dm_id']
    remove_dm(token, dm_id)
    return dumps({})

                                                               
'''
user routes
'''

@APP.route("/user/profile/v2", methods=['GET'])
def get_user_profile():
    '''
    GET user profile
    '''
    

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    userprofile = user_profile(token, int(u_id))
    return dumps(userprofile)

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_setname():    
    '''
    update username
    '''
    user_info = request.get_json()

    token = user_info['token']
    name_first = user_info['name_first']
    name_last = user_info['name_last']

    user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_setemail():    
    '''
    update email
    '''
    user_info = request.get_json()

    token = user_info['token']
    email = user_info['email']

    user_profile_setemail(token, email)
    return dumps({})

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_sethandle():    
    '''
    update handle
    '''
    user_info = request.get_json()

    token = user_info['token']
    new_handle = user_info['handle_str']

    user_profile_sethandle(token, new_handle)
    return dumps({})

@APP.route("/users/all/v1", methods=['GET'])
def get_users_all():   
    '''
    Returns a list of all users and their associated details
    '''


    token = request.args.get('token')

    all_users_info = users_all(token)
    return dumps (all_users_info)


@APP.route("/static/<filename>", methods=['GET'])
def getprofilephoto_flask(filename):
    
    
    return send_from_directory('static', filename)


@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def upload_photo(): 
    '''
    upload photo for user
    '''
    user_info = request.get_json()
    token = user_info['token']
    img_url = user_info['img_url']
    x_start = user_info['x_start']
    y_start = user_info['y_start']
    x_end = user_info['x_end']
    y_end = user_info['y_end']
    
    user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    return dumps({})

@APP.route("/user/stats/v1", methods=['GET'])
def user_stat():
    token = request.args.get('token')
    stat_info = user_stats(token)
    return dumps(stat_info)

@APP.route("/users/stats/v1", methods=['GET'])
def users_stat():
    token = request.args.get('token')
    stat_info = users_stats(token)
    return dumps(stat_info)


'''
message routes
'''
@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    '''
    send message
    '''
    message_info = request.get_json()
    token = message_info['token']
    channel_id = message_info['channel_id']
    message = message_info['message']
    ret = send_message(token, channel_id, message)
    return dumps(ret)

@APP.route("/message/edit/v2", methods=['PUT'])
def message_edit():
    '''
    edit message
    '''
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    message = message_info['message']
    edit_message(token, message_id, message)
    return dumps({})

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    '''
    remove message
    '''
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    
    remove_message(token, message_id)
    return dumps({})

@APP.route("/message/senddm/v1", methods=['POST'])
def dm_send():
    '''
    send dm
    '''
    message_info = request.get_json()
    token = message_info['token']
    dm_id = message_info['dm_id']
    message = message_info['message']
    ret = send_dm(token, dm_id, message)
    return dumps(ret)

@APP.route('/message/share/v1', methods=['POST'])
def message_share():
    message_info = request.get_json()
    token = message_info['token']
    og_mes_id = message_info['og_message_id']
    message = message_info['message']
    channel_id = message_info['channel_id']
    dm_id = message_info['dm_id']
    result = share_message(token, og_mes_id, message, channel_id, dm_id)
    return dumps(result)

@APP.route('/message/sendlater/v1', methods=['POST'])
def message_sendlater():
    message_info = request.get_json()
    token = message_info['token']
    channel_id = message_info['channel_id']
    message = message_info['message']
    time = message_info['time_sent']
    result = sendlater_message(token, channel_id, message, time)
    return dumps(result)

@APP.route('/message/sendlaterdm/v1', methods=['POST'])
def message_sendlaterdm():
    message_info = request.get_json()
    token = message_info['token']
    dm_id = message_info['dm_id']
    message = message_info['message']
    time = message_info['time_sent']
    result = sendlaterdm_message(token, dm_id, message, time)
    return dumps(result)
    
@APP.route("/message/react/v1", methods=['POST'])
def react():
    
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    react_id = message_info['react_id']
    
    message_react(token, message_id, react_id)
    return dumps({})
    
@APP.route("/message/unreact/v1", methods=['POST'])
def unreact():
    
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    react_id = message_info['react_id']
    
    message_unreact(token, message_id, react_id)
    return dumps({})
           
@APP.route("/message/pin/v1", methods=['POST'])
def pin():
    
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    
    message_pin(token, message_id)
    return dumps({})

@APP.route("/message/unpin/v1", methods=['POST'])
def unpin():
    
    message_info = request.get_json()
    token = message_info['token']
    message_id = message_info['message_id']
    
    message_unpin(token, message_id)
    return dumps({})    
    
    

'''
notification routes
'''
@APP.route('/notifications/get/v1', methods=['GET'])
def noti_read():
    
    token = request.args.get('token')
    notifications = read_notifications(token)
    return dumps(notifications)
    
'''
admin routes
'''

@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def admin_rm():
    args = request.get_json()
    token = args['token']
    u_id = args['u_id']
    remove(token, u_id)
    return dumps({})

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def admin_userper():
    args = request.get_json()
    token = args['token']
    u_id = args['u_id']
    permission_id = args['permission_id']
    userpermission(token, u_id, permission_id)
    return dumps({})

'''
standup routes
'''
@APP.route('/standup/start/v1', methods=['POST'])
def stdup_start():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    length = args['length']
    time_finish = standup_start(token, int(channel_id), length)
    return dumps(time_finish)

@APP.route('/standup/active/v1', methods=['GET'])
def stdup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    active_details = standup_active(token, int(channel_id))
    return dumps(active_details)

@APP.route('/standup/send/v1', methods=['POST'])
def stdup_send():
    args = request.get_json()
    token = args['token']
    channel_id = args['channel_id']
    message = args['message']
    standup_send(token, int(channel_id), message)
    return dumps({})


'''
other routes
'''

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    '''
    Resets the internal data of the application to it's initial state
    '''
    clear_v1()
    
    return dumps({})

@APP.route('/search/v2', methods=['GET'])
def search():
    
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    result = search_v2(token, query_str)
    return dumps(result)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
