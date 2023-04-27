import requests
from pprint import pprint
import json
from datetime import datetime
import time

"""
https://oauth.vk.com/authorize?client_id=51589391&display=page&scope=photos&response_type=token&v=5.131
"""


class VkToYadisk:
    vk_url = 'https://api.vk.com/method/'

    def __init__(self):
        self.vktoken = vktoken
        self.yatoken = yatoken
        self.id = vk_id

    def load_photo_inf_from_vk(self):
        load_url = self.vk_url + 'photos.getAll'
        params = {
            'user_ids': self.id,
            'access_token': self.vktoken,
            'v': '5.131',
            'extended': '1'
        }
        result = (requests.get(load_url, params=params)).json()
        return result


    def do_photo_list (self):
        photo_list = []
        for items in photo_inf['response']['items']:
            photo_dict = {'id': '', 'date': '', 'likes': '', 'url': ''}
            photo_dict['id'] = items['id']
            photo_dict['date'] = str(datetime.fromtimestamp(items['date']).strftime('%d - %m - %y'))
            photo_dict['likes'] = items['likes']['count']
            for size in items['sizes']:
                if size['type'] == 'x':
                    photo_dict['url'] = size['url']
                if size['type'] == 'z':
                    photo_dict['url'] = size['url']
            photo_list.append(photo_dict)
        with open('photos.json', 'w', encoding='utf-8') as res_file:
            json.dump(photo_list, res_file, indent=1)
        return photo_list


    def post_photo_to_disk(self):
        ya_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.yatoken}'}
        params = {'path': 'photo_from_vk'}
        requests.put(ya_url, headers=headers, params=params)    # Создаем папку
        for photo in photo_list:
            path = f"photo_from_vk/Likes-{photo['likes']}_Date-{photo['date']}"
            url = photo['url']
            params = {'path': path, 'url': url}
            requests.post(ya_url + 'upload/', headers=headers, params=params)
            time.sleep(3)
        return 'Загрузка на Я.Диск завершена '


if __name__=='__main__':
    with open('tokenVK.txt') as file:
        vktoken=file.read()
    with open('tokenYa.txt') as file:
        yatoken = file.read()
    vk_id = '513053501'
    vktoya = VkToYadisk()
    photo_inf = vktoya.load_photo_inf_from_vk()
    photo_list = vktoya.do_photo_list()
    photo_post = vktoya.post_photo_to_disk()

