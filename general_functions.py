from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import os

def get_file_extension(img_url):
    parsed_url = urlparse(img_url)
    cropped_url = f"{parsed_url.path}"
    unqoute_url = unquote(cropped_url)
    divided_url = os.path.split(unqoute_url)
    return divided_url[1]

def save_img(img_url, name_img):
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'images/{name_img}', 'wb') as file:
        file.write(response.content)
