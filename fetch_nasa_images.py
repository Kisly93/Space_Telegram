import requests
import os
from urllib.parse import urlparse
from urllib.parse import unquote
from dotenv import load_dotenv
from pathlib import Path
import argparse


def get_nasa_images(api_key, count_photo):
    payload = {
        'api_key': api_key,
        'count': count_photo
    }
    link = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(link, params=payload)
    response.raise_for_status()
    return response.json()


def get_file_extension(img_url):
    parsed_nasa = urlparse(img_url)
    cropped_nasa = f"{parsed_nasa.path}"
    unqoute_nasa = unquote(cropped_nasa)
    split_nasa = os.path.split(unqoute_nasa)
    return split_nasa[1]


def save_nasa_img(img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'images/{get_file_extension(img_url)}', 'wb') as file:
        file.write(response.content)


def main():
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
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
        save_nasa_img(img_url)


if __name__ == '__main__':
    main()
