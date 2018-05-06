import requests
import time
import json

with open('vk_token') as f:
    TOKEN = f.read().strip()

TOO_MANY_REQUESTS = 6
USER_HAS_BEED_BANNED_OR_DELETED = 18
NO_PERMISSION_TO_PERFORM_THIS_ACTION = 7

def make_request(method, **kwargs):
    params = {
        'access_token': TOKEN,
        'v': '5.74'
    }
    params = {**params, **kwargs}

    while True:
        response = requests.get(f'https://api.vk.com/method/{method}', params).json()

        if 'error' in response:
            error = response['error']
            if error["error_code"] == TOO_MANY_REQUESTS:
                time.sleep(0.2)
                continue
            elif error["error_code"] == NO_PERMISSION_TO_PERFORM_THIS_ACTION:
                print(error["error_msg"])
                return None
            elif error["error_code"] == USER_HAS_BEED_BANNED_OR_DELETED:
                print(error["error_msg"])
                return None
            else:
                print("Произошла неизвестная ошибка")
                return None
        else:
            return response['response']


def get_user(id_or_screen_name):
    user_id = make_request('users.get', user_ids=id_or_screen_name)
    return user_id[0]['id']


def get_friends(id_or_screen_name):
    friends = make_request('friends.get', user_id=id_or_screen_name)
    return friends


def get_groups(id_or_screen_name):
    groups = make_request('groups.get', user_id=id_or_screen_name)
    return groups

def get_friend_groups(user_id):
    publics = set()
    user_id = get_user(user_id)
    user_friends = get_friends(user_id)['items']
    user_groups = set(get_groups(user_id)['items'])

    for i, friend in enumerate(user_friends):
        friend_groups = get_groups(friend)

        if friend_groups is None:
            print(i, f'vk.com/id{friend}', friend_groups)
        else:
            publics.update(friend_groups['items'])
            print(i, f'vk.com/id{friend}', friend_groups['items'])

    only_groups = user_groups - publics
    return only_groups


def show_publics(user_id):
    only_groups = get_friend_groups(user_id)
    group_list = []

    for group in only_groups:
        only_group_json = make_request('groups.getById', group_id=group, fields='members_count')[0]
        group_list.append({
            'name': only_group_json['name'],
            'gid': only_group_json['id'],
            'members_count': only_group_json['members_count']
        })

        print('-*- loading -*- creating groups.json -*-')

    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)



print(show_publics('tim_leary'))
