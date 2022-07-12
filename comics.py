import os
import random

import requests
from dotenv import load_dotenv

from comics_helper import create_url, download_picture


def upload_picture_to_server(vk_group_id, vk_access_token, picture):
    payload = {'group_id': vk_group_id,
               'access_token': vk_access_token,
               'v': 5.131                           # последняя версия API
               }
    response = requests.get(create_url(method='photos.getWallUploadServer'),
                            params=payload)
    response.raise_for_status()
    with open(picture, 'rb') as file:
        upload_url = response.json()['response']['upload_url']
        files = {
            'photo': file,
        }
        picture_response = requests.post(upload_url, files=files)
        picture_response.raise_for_status()
        return picture_response.json()


def upload_picture_to_album(vk_group_id, vk_access_token, params_picture):
    picture_in_album_payload = {'group_id': vk_group_id,
                                'access_token': vk_access_token,
                                'hash': params_picture['hash'],      # данные полученные от функции  upload_image_to_server
                                'photo': params_picture['photo'],    # данные полученные от функции  upload_image_to_server
                                'server': params_picture['server'],  # данные полученные от функции  upload_image_to_server
                                'v': 5.131                           # последняя версия API
                                }
    picture_in_album_response = requests.post(create_url('photos.saveWallPhoto'),
                                              params=picture_in_album_payload)
    picture_in_album_response.raise_for_status()
    return picture_in_album_response.json()['response'][0]


def post_picture_to_wall(vk_access_token, vk_group_id, owner_id, media_id, comics_comment):
    post_picture_payload = {'access_token': vk_access_token,
                            'owner_id': f'-{vk_group_id}',                 # значение должно быть со знаком "-"
                            'from_group': 1,                               # 1 - от имени группы, 0 - от имени пользователя
                            'attachments': f'photo{owner_id}_{media_id}',  # переменные берутся по результату работы функции upload_picture_to_album
                            'message': comics_comment,                     # комментарий со страницы xkcd комикса
                            'v': 5.131                                     # последняя версия API
                            }
    post_picture_response = requests.post(create_url('wall.post'),
                                          params=post_picture_payload)
    post_picture_response.raise_for_status()
    return post_picture_response.json()


if __name__ == '__main__':
    load_dotenv()
    vk_id = os.environ['VK_ID']
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']

    xkcd_url = f'https://xkcd.com/{random.randint(1, 2644)}/info.0.json'
    xkcd_response = requests.get(xkcd_url)
    comics_page = xkcd_response.json()
    download_picture(picture_url=comics_page['img'],
                     picture_path='comics')

    picture_page = upload_picture_to_album(vk_group_id,
                                           vk_access_token,
                                           params_picture=upload_picture_to_server(vk_group_id,
                                                                                   vk_access_token,
                                                                                   picture='comics.jpg'))

    post_picture_to_wall(vk_access_token,
                         vk_group_id,
                         owner_id=picture_page['owner_id'],
                         media_id=picture_page['id'],
                         comics_comment=comics_page['alt'])

    os.remove('comics.jpg')
