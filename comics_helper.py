import requests


def download_picture(picture_url, picture_path):
    picture_response = requests.get(picture_url)
    picture_response.raise_for_status()
    with open(f'{picture_path}.jpg', 'wb') as file:
            file.write(picture_response.content)


def create_url(method):
    url = f'https://api.vk.com/method/{method}'
    return url



