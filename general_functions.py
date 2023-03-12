from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import os

def get_file_extension(img_url):
    parsed_nasa = urlparse(img_url)
    cropped_nasa = f"{parsed_nasa.path}"
    unqoute_nasa = unquote(cropped_nasa)
    split_nasa = os.path.split(unqoute_nasa)
    return split_nasa[1]

def save_img(img_url, name_img):
    directory = Path(r'images').mkdir(parents=True, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'images/{name_img}', 'wb') as file:
        file.write(response.content)
