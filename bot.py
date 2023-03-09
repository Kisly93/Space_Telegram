import random
import os
import argparse
import time
import telegram
from dotenv import load_dotenv


def send_img(token, chat_id, time_interval, img_space):
    bot = telegram.Bot(token=token)

    for img in img_space:
        with open(f'images/{img}', 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        time.sleep(time_interval)


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID_TG')
    token = os.getenv('TOKEN_TELEGRAM')

    parser = argparse.ArgumentParser(
        description='Введите время через которое бот публикует фотографии в секундах'
    )
    parser.add_argument('sec', nargs='?', type=int, default=14000)
    args = parser.parse_args()
    time_interval = args.sec

    img_space = os.listdir('images')

    while send_img(token, chat_id, time_interval, img_space):
        random.shuffle(img_space)


if __name__ == '__main__':
    main()
