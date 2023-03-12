import requests
import argparse
from pathlib import Path


def fetch_spacex_links_id(id_space):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{id_space}')
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def save_spacex_img(name, img):
    response = requests.get(img)
    response.raise_for_status()
    with open(f'images/{name}', 'wb') as file:
        file.write(response.content)


def main():
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Скрипт скачивает снимки с запуска SpaceX '
    )
    parser.add_argument('id', nargs='?', default='latest', help='id запуска, если нет id - качает снимки с последнего запуска')
    args = parser.parse_args()
    id_launch = args.id
    try:
        for num, img in enumerate(fetch_spacex_links_id(id_launch)):
            name = f'space{num}.jpg'
            save_spacex_img(name, img)

    except requests.exceptions.HTTPError as error:
        print("Вы ввели неправильный id.")


if __name__ == '__main__':
    main()
