from urllib.parse import urlencode
import requests
from pprint import pprint
import time
import json

TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
id = 'georgerailz'

def make_request(method, **kwargs,):
    params = {
        'access_token': TOKEN,
        'v': '5.74'
    }
    params = {**params, **kwargs}
    response = requests.get(f'https://api.vk.com/method/{method}', params)
    return response

    # if response.json()['response'] == True:
    #     return response
    # elif response.json()['error']==True and response.json()['error']['error_code']==18:
    #     print('User was deleted or banned')
    #     return
    # elif response.json()['error']==True and response.json()['error']['error_code']==10:
    #     time.sleep(1)
    #     return response


def get_user(id_or_screen_name):
    user_id = make_request('users.get', user_ids=id_or_screen_name)
    return user_id.json()['response'][0]['id']

def get_friends(id_or_screen_name):
    friends = make_request('friends.get', user_id=id_or_screen_name)
    return friends.json()

    # try:
    #     friends_dict = friends.json()['response']
    #     return set(friends_dict['items'])
    # except KeyError:
    #     error = friends.json()['error']
    #     print(f'Ошибка № {error["error_code"]} {error["error_msg"]}')

def get_groups(id_or_screen_name):
    groups = make_request('groups.get', user_id=id_or_screen_name)
    return groups.json()

    # try:
    #     groups_dict = groups.json()['response']
    #     return set(groups_dict['items'])
    # except KeyError:
    #     error = groups.json()['error']
    #     print(f'Ошибка № {error["error_code"]} {error["error_msg"]}')
    #     get_groups(id_or_screen_name)

def get_friend_groups(user_id):
    publics = set()
    user_id = get_user(user_id)
    user_friends = get_friends(user_id)['response']['items']
    user_groups = get_groups(user_id)['response']['items']
    time.sleep(1)

    for i, friend in enumerate(user_friends):
        try:
            friend_groups = get_groups(friend)['response']['items']
            publics.update(friend_groups)
            print(i, f'vk.com/id{friend}', friend_groups)
            time.sleep(0.35)
        except KeyError:
            print(i, f'vk.com/id{friend} User was banned or deleted')

    only_groups = set(user_groups) - publics
    return only_groups

print(get_friend_groups(id))



