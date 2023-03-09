import requests
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote
import datetime
from dotenv import load_dotenv
import argparse


def fetch_epic_info(api_key, latest_epic_image_url):
    payload = {
        'api_key': api_key
    }
    response = requests.get(latest_epic_image_url, params=payload)
    response.raise_for_status()
    return response.json()


def get_epic_img(api_key, epic_image_archive_url, format_date, epic_image):
    payload = {
        'api_key': api_key
    }
    response = requests.get(f'{epic_image_archive_url}/{format_date}/png/{epic_image}.png', params=payload)
    response.raise_for_status()
    return response.url


def cut_epic_img(url):
    parsed_nasa = urlparse(url)
    cropped_nasa = f"{parsed_nasa.path}"
    unqoute_nasa = unquote(cropped_nasa)
    split_nasa = os.path.split(unqoute_nasa)
    return split_nasa[1]


def fetch_epic_photo(api_key, link_two, format_date, epic_image):
    url = get_epic_img(api_key, link_two, format_date, epic_image)
    response = requests.get(url)
    response.raise_for_status()
    with open(f'images/{cut_epic_img(url)}', 'wb') as file:
        file.write(response.content)


def main():
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Введите количество фото'
    )
    parser.add_argument('count', nargs='?', default='1', type=int)
    args = parser.parse_args()
    count_photo = args.count
    load_dotenv()
    api_key = os.getenv('API_KEY_SPACE')
    latest_epic_image_url = 'https://api.nasa.gov/EPIC/api/natural'
    epic_image_archive_url = 'https://api.nasa.gov/EPIC/archive/natural'
    get_epic = fetch_epic_info(api_key, latest_epic_image_url)
    for photo_info in get_epic[:count_photo]:
        epic_date = photo_info['date']
        epic_image = photo_info['image']
        old_date = datetime.datetime.strptime(epic_date, "%Y-%m-%d %H:%M:%S").date()
        format_date = datetime.datetime.strftime(old_date, "%Y/%m/%d")
        fetch_epic_photo(api_key, epic_image_archive_url, format_date, epic_image)


if __name__ == '__main__':
    main()
