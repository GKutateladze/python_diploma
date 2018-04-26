import requests
import time
import json

with open('vk_token') as f:
    TOKEN = f.readline()

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

def get_groups(id_or_screen_name):
    groups = make_request('groups.get', user_id=id_or_screen_name)
    return groups.json()

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

def show_publics(user_id):
    only_groups = get_friend_groups(user_id)
    group_list = []
    for group in only_groups:
        try:
            only_group_json = make_request('groups.getById', group_id=group, fields='members_count').json()['response'][0]
            time.sleep(0.35)

            group_list.append({
                'name': only_group_json['name'],
                'gid': only_group_json['id'],
                'members_count': only_group_json['members_count']
            })
            print('-*- loading -*- creating groups.json -*-')
        except:
            print('Oops, error occured')

    with open('groups.json', 'w', encoding='utf8') as f:
        data = json.dump(group_list, f, ensure_ascii=False, indent=2)
        return data

id = 'tim_leary'
print(show_publics(id))
