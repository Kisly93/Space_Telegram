import requests
import argparse
from pathlib import Path


def fetch_space_links_id(id_space):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{id_space}')
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def fetch_spacex_last_launch(name, img):
    response = requests.get(img)
    response.raise_for_status()
    with open(f'images/{name}', 'wb') as file:
        file.write(response.content)


def main():
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='С помощью скрипта можно скачать снимки с запуска SpaceX. Введите id запуска: '
    )
    parser.add_argument('id', nargs='?', default='latest')
    args = parser.parse_args()
    id_launch = args.id
    try:
            fetch_space_links_id(id_launch)
            for num, img in enumerate(fetch_space_links_id(id_launch)):
                name = f'space{num}.jpg'
                fetch_spacex_last_launch(name, img)

    except requests.exceptions.HTTPError as error:
        print("Вы ввели неправильный id.")


if __name__ == '__main__':
    main()
