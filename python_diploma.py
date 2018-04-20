from urllib.parse import urlencode
import requests
from pprint import pprint
import time
import json

APP_ID = 6453204
AUTH_URL = 'https://oauth.vk.com/authorize'

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'scope': 'friends,groups,status',
    'response_type': 'token',
    'v': '5.74'
}

# print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = 'c61e614f574a38a3cca91799c62c739cddc468cbb59919ae0239ce7c0508cb5ece80969b6f5674c7d4909'
NETOLOGY_TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd 494db19099'

USER_ID = "georgerailz"

def find_user(id_or_screen_name):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'user_ids': id_or_screen_name
    }
    user_id = requests.get('https://api.vk.com/method/users.get', params).json()['response'][0]['id']
    return user_id

def friends_list(user_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'user_id': user_id
    }
    response = requests.get('https://api.vk.com/method/friends.get', params).json()['response']['items']
    return response

def groups_list(user_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'user_id': user_id
    }
    response = set(requests.get('https://api.vk.com/method/groups.get', params).json()['response']['items'])
    return response

group_set = []
for friend in enumerate(friends_list(find_user(USER_ID))):
    try:
        grp = groups_list(find_user(friend))
        time.sleep(1)
        group_set.append(grp)
        print(friend, grp)
    except:
        print(' --- ACOUNT HAS BEEN BLOCKED OR DELETED BY THE USER --- ')
print('FINISHED')

product = groups_list(find_user(USER_ID))
for set in group_set:
    product = product - set

def show_publics(public_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'group_id': public_id,
    }
    publics = requests.get('https://api.vk.com/method/groups.getById', params).json()['response']
    return publics

def num_members(public_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'group_id': public_id,
    }
    publics = requests.get('https://api.vk.com/method/groups.getMembers', params).json()['response']
    return publics

final_list = []
for i in product:
    id = show_publics(i)[0]['id']
    name = show_publics(i)[0]['name']
    count = num_members(i)['count']
    # final_dict = {
    #     'id': id,
    #     'name': name,
    #     'count': count
    # }
    # final_list.append(final_dict)
    print('ID: ', id)
    print('Name: ', name)
    print('Count: ', count)
    print('--------------')
    time.sleep(2)
#
# print(final_dict)