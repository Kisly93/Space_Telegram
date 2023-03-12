import requests
import os
import datetime
from dotenv import load_dotenv
import argparse
from general_functions import get_file_extension
from general_functions import save_img


def fetch_epic_catalog(api_key, latest_epic_image_url):
    payload = {
        'api_key': api_key
    }
    url = latest_epic_image_url
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_epic_img(api_key, epic_image_archive_url, date_format, epic_image):
    payload = {
        'api_key': api_key
    }
    url = f'{epic_image_archive_url}/{date_format}/png/{epic_image}.png'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.url


def main():
    parser = argparse.ArgumentParser(
        description='Cкрипт скачивает снимки NASA нашей планеты'
    )
    parser.add_argument('count', nargs='?', default='1', type=int, help='количество скачиваемых снимков')
    args = parser.parse_args()
    count_images = args.count
    load_dotenv()
    api_key = os.getenv('API_KEY_NASA')
    latest_epic_image_url = 'https://api.nasa.gov/EPIC/api/natural'
    epic_image_archive_url = 'https://api.nasa.gov/EPIC/archive/natural'
    get_epic = fetch_epic_catalog(api_key, latest_epic_image_url)
    for image_details in get_epic[:count_images]:
        epic_date = image_details['date']
        epic_image = image_details['image']
        old_date = datetime.datetime.strptime(epic_date, "%Y-%m-%d %H:%M:%S").date()
        date_format = datetime.datetime.strftime(old_date, "%Y/%m/%d")
        img_url = get_epic_img(api_key, epic_image_archive_url, date_format, epic_image)
        name_img = get_file_extension(img_url)
        save_img(img_url, name_img)


if __name__ == '__main__':
    main()
