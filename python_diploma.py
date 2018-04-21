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

TOKEN = '958bd3974dd9acfce97a36e3d359e4605bafdaab11302720ee8411adbce241273168395bf694b87af0060'
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

print(product)

def show_publics(public_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'group_id': public_id,
    }
    publics = requests.get('https://api.vk.com/method/groups.getById', params).json()
    return publics

def num_members(public_id):
    params = {
        'access_token': TOKEN,
        'v': '5.74',
        'group_id': public_id,
    }
    publics = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
    return publics

publics = []
for i in product:
    id = show_publics(i)
    name = show_publics(i)
    count = num_members(i)

    public_dict = {
        'id': id['response'][0]['id'],
        'name': name['response'][0]['name'],
        'count': count['response']['count']
    }

    public_dict = json.dumps(public_dict, ensure_ascii=False)
    public_dict = json.loads(public_dict)
    print('-- thinking --')
    publics.append(public_dict)
    time.sleep(1)

pprint(publics)
