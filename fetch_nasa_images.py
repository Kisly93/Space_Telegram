import requests
import os
from dotenv import load_dotenv
import argparse
from general_functions import get_file_extension
from general_functions import save_img


def get_nasa_images(api_key, count_photo):
    payload = {
        'api_key': api_key,
        'count': count_photo
    }
    link = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(link, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт скачивает снимки NASA, которые пуюликуюся каждый день '
    )
    parser.add_argument('count', nargs='?', default='5', type=int, help='количество скачиваемых снимков')
    args = parser.parse_args()
    count_images = args.count
    load_dotenv()
    api_key = os.getenv('API_KEY_NASA')
    for nasa_image_details in get_nasa_images(api_key, count_images):
        img_url = nasa_image_details['url']
        name_img = get_file_extension(img_url)
        save_img(img_url, name_img)


if __name__ == '__main__':
    main()
