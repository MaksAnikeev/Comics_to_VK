import os
import random

import requests
from dotenv import load_dotenv


def download_picture(picture_url, picture_path):
    picture_response = requests.get(picture_url)
    picture_response.raise_for_status()
    with open(f'{picture_path}.jpg', 'wb') as file:
            file.write(picture_response.content)


def upload_picture_to_server(vk_group_id, vk_access_token, picture):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {'group_id': vk_group_id,
               'access_token': vk_access_token,
               'v': vk_api_version
               }
    response = requests.get(url, params=payload)
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
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    picture_in_album_payload = {'group_id': vk_group_id,
                                'access_token': vk_access_token,
                                'hash': params_picture['hash'],      # данные полученные от функции  upload_image_to_server
                                'photo': params_picture['photo'],    # данные полученные от функции  upload_image_to_server
                                'server': params_picture['server'],  # данные полученные от функции  upload_image_to_server
                                'v': vk_api_version
                                }
    picture_in_album_response = requests.post(url, params=picture_in_album_payload)
    picture_in_album_response.raise_for_status()
    return picture_in_album_response.json()['response'][0]


def post_picture_to_wall(vk_access_token, vk_group_id, owner_id, media_id, comics_comment):
    url = 'https://api.vk.com/method/wall.post'
    post_picture_payload = {'access_token': vk_access_token,
                            'owner_id': f'-{vk_group_id}',                 # значение должно быть со знаком "-"
                            'from_group': 1,                               # 1 - от имени группы, 0 - от имени пользователя
                            'attachments': f'photo{owner_id}_{media_id}',  # переменные берутся по результату работы функции upload_picture_to_album
                            'message': comics_comment,                   
                            'v': vk_api_version
                            }
    post_picture_response = requests.post(url, params=post_picture_payload)
    post_picture_response.raise_for_status()
    return post_picture_response.json()


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_api_version = '5.131'

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
