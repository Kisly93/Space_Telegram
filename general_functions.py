from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import os

def get_file_extension(img_url):
    parsed_url_nasa = urlparse(img_url)
    cropped_url_nasa = f"{parsed_url_nasa.path}"
    unqoute_url_nasa = unquote(cropped_url_nasa)
    split_url_nasa = os.path.split(unqoute_url_nasa)
    return split_url_nasa[1]

def save_img(img_url, name_img):
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'images/{name_img}', 'wb') as file:
        file.write(response.content)
