import requests
import os
from urllib.parse import urlparse
from urllib.parse import unquote
from dotenv import load_dotenv
from pathlib import Path
import argparse


def get_nasa_img(api_key, count_photo):
    payload = {
        'api_key': api_key,
        'count': count_photo
    }
    link = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(link, params=payload)
    return response.json()


def cut_nasa_img(img_url):
    parsed_nasa = urlparse(img_url)
    cropped_nasa = f"{parsed_nasa.path}"
    unqoute_nasa = unquote(cropped_nasa)
    split_nasa = os.path.split(unqoute_nasa)
    return split_nasa[1]


def get_latest_nasa_img(img_url):
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'images/{cut_nasa_img(img_url)}', 'wb') as file:
        file.write(response.content)


def main():
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='С помощью скрипта можно скачать снимки NASA, которые пуюликуюся каждый день. Введите количество снимков: '
    )
    parser.add_argument('count', nargs='?', default='5', type=int)
    args = parser.parse_args()
    count_photo = args.count
    load_dotenv()
    api_key = os.getenv('API_KEY_NASA')
    for nasa_image_details in get_nasa_img(api_key, count_photo):
        img_url = nasa_image_details['url']
        cut_nasa_img(img_url)
        get_latest_nasa_img(img_url)


if __name__ == '__main__':
    main()
