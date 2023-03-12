import requests
import argparse
from general_functions import save_img


def fetch_spacex_links_id(id_space):
    url = f'https://api.spacexdata.com/v5/launches/{id_space}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт скачивает снимки с запуска SpaceX '
    )
    parser.add_argument('id', nargs='?', default='latest',
                        help='id запуска, если нет id - качает снимки с последнего запуска')
    args = parser.parse_args()
    id_launch = args.id
    try:
        for num, img_url in enumerate(fetch_spacex_links_id(id_launch)):
            name_img = f'space{num}.jpg'
            save_img(img_url, name_img)

    except requests.exceptions.HTTPError as error:
        print("Вы ввели неправильный id.")


if __name__ == '__main__':
    main()
