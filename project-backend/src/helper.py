import jwt
import pickle
import src.error as error
import src.auth as auth
# set secret for jwt
SECRET = "Sunshine"

data = {
    'users': [],
    'channels': [],
    'messages': [],
    'dms':[],
    'dreams_stats':{'channels_exist':[],'dms_exist':[],'messages_exist':[]},
    'standups':[],
}

#generate user_id from token
def getUserId(token):
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms= ['HS256'])
    u_id = int(decoded['user_id'])
    return u_id
    
# check if the toke passed in is valid
def check_token_valid(token):
    global SECRET
    data = load_data()
    
    try:
        jwt.decode(token, SECRET, algorithms= ['HS256'])
    except jwt.exceptions.InvalidSignatureError as token_invalid:
        raise error.AccessError(description= "token invalid") from token_invalid
    except jwt.exceptions.DecodeError as token_empty:
        raise error.AccessError(description= "token invalid") from token_empty
    
    dataStruc = auth.retrieve_session(token)
    tokenSessionid = dataStruc['session_id']
    u_id = dataStruc['user_id']
    for user in data['users']:
        if token == user['token'] and u_id == user['u_id']:
            if tokenSessionid in user['sessionList']:
                return True
            else: 
                raise error.AccessError(description= "token invalid, logged out")
            
    return False
           
def load_data():
    global data
    try:
        data = pickle.load(open("database.p", "rb"))    
    except Exception:
	    pass
    return data

def save_data(data):
    with open('database.p', 'wb') as FILE:
        pickle.dump(data, FILE)
    return data
