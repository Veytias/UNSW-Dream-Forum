import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
import src.error
from src.helper import load_data    

def test_clear_success():  
    clear_v1()
    auth_register_v2('first1email@gmail.com', '12345Hello', 'Inviter', 'surname')
    clear_v1()
    data = load_data()
    assert (len(data['users']) == 0 and len(data['channels']) == 0 and len(data['messages']) == 0)
    
