import requests
from src import config
BASE_URL =  config.url

def test_clear_success(): 
    clear1 = requests.delete(f"{BASE_URL}/clear/v1")
    user = requests.post(f"{BASE_URL}/auth/register/v2", json={
        'email': 'z1234567@gmail.com',
        'password': 'z1234567',
        'name_first': 'Nintendo',
        'name_last': 'Switch'
    })
    payload0 =  user.json()
    requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': payload0['token'],
        'name': 'Test Channel',
        'is_public': True
    })
    clear2 = requests.delete(f"{BASE_URL}/clear/v1")
    channel_info = requests.get(f"{BASE_URL}/channels/list/v2?token={payload0['token']}")

    assert clear1.status_code == 200
    assert user.status_code == 200
    assert clear2.status_code == 200
    assert channel_info.status_code == 500
