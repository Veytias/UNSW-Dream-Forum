import pytest
from src.auth import auth_register_v2 as register
from src.dm import dm_create_v1,dm_list_v1
from src.other import clear_v1
import src.error

'''
Success case
'''

def test_succes_dm_list():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jack", "Smith")
    user_2 = register("user_2@gmail.com","678901", "Ant", "Jame")
    dm_create_v1(user_1['token'],[user_2['auth_user_id']])
    dm_1 = dm_list_v1(user_1['token'])
    expected = {'dms' : [{'dm_id': 1,'name': "antjame, jacksmith"}]}
    assert dm_1 == expected

def test_user_in_multi_dm():
    clear_v1()
    user_1 = register("user_1@gmail.com","123456", "Jack", "Smith")
    user_2 = register("user_2@gmail.com","678901", "Ant", "Jame")
    user_3 = register("user_3@gmail.com","987654", "Zebra", "Bird")
    dm_create_v1(user_1['token'],[user_2['auth_user_id']])
    dm_create_v1(user_3['token'],[user_2['auth_user_id']])
    dm_2 = dm_list_v1(user_2['token'])
    expected = {'dms' : [{'dm_id': 1,'name': "antjame, jacksmith"}
                        ,{'dm_id': 2,'name': "antjame, zebrabird"}]}
    assert dm_2 == expected


    
