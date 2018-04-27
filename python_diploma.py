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
    response = requests.get(f'https://api.vk.com/method/{method}', params).json()

    for key in response.keys():
        if key == 'response':
            return response
        elif key == 'error':
            error = response['error']
            if error["error_code"] == 6:
                time.sleep(2)
                response = requests.get(f'https://api.vk.com/method/{method}', params).json()
                return response
            elif error["error_code"] == 7:
                return error["error_msg"]
            elif error["error_code"] == 18:
                return error["error_msg"]


def get_user(id_or_screen_name):
    user_id = make_request('users.get', user_ids=id_or_screen_name)
    return user_id['response'][0]['id']

def get_friends(id_or_screen_name):
    friends = make_request('friends.get', user_id=id_or_screen_name)
    return friends

def get_groups(id_or_screen_name):
    groups = make_request('groups.get', user_id=id_or_screen_name)
    return groups

def get_friend_groups(user_id):
    publics = set()
    user_id = get_user(user_id)
    user_friends = get_friends(user_id)['response']['items']
    user_groups = get_groups(user_id)['response']['items']

    for i, friend in enumerate(user_friends):
        friend_groups = get_groups(friend)
        
        try:
            publics.update(friend_groups['response']['items'])
            print(i, f'vk.com/id{friend}', friend_groups)
        except:
            publics.update(friend_groups)
            print(i, f'vk.com/id{friend}', friend_groups)
            
    only_groups = set(user_groups) - publics
    return only_groups

def show_publics(user_id):
    only_groups = get_friend_groups(user_id)
    group_list = []
    
    for group in only_groups:
        only_group_json = make_request('groups.getById', group_id=group, fields='members_count')['response'][0]
        group_list.append({
            'name': only_group_json['name'],
            'gid': only_group_json['id'],
            'members_count': only_group_json['members_count']
        })
        
        print('-*- loading -*- creating groups.json -*-')

    with open('groups.json', 'w', encoding='utf8') as f:
        data = json.dump(group_list, f, ensure_ascii=False, indent=2)
        return data

print(show_publics('tim_leary'))
