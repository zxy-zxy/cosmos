import os
import sys

from dotenv import load_dotenv
from instabot import Bot

from utils.common import (
    IMAGE_DIRECTORY_ROOT,
    SPACEX_DIRECTORY_NAME,
    HUBBLE_DIRECTORY_NAME
)
from utils.img_processing import fix_photo


def create_bot_instance():
    instagram_login = os.getenv('instagram_login')
    instagram_password = os.getenv('instagram_password')
    bot = Bot()
    loggged_in_succesfully = bot.login(
        username=instagram_login,
        password=instagram_password)
    if loggged_in_succesfully:
        return bot
    return None


def post_photos_from_directory(directory, bot: Bot):
    for root, dirs, file_names in os.walk(directory):
        for name in file_names:
            source_image_filename = os.path.join(root, name)
            photo = fix_photo(source_image_filename)
            bot.upload_photo(photo, caption=os.path.split(root)[-1])


if __name__ == '__main__':
    load_dotenv()

    bot = create_bot_instance()

    if bot is None:
        sys.exit('''
        Cannot log-in with provided credentials.
        Check instagram_login and instagram_password env variables.
        ''')

    spacex_directory = os.path.join(IMAGE_DIRECTORY_ROOT, SPACEX_DIRECTORY_NAME)
    if not os.path.isdir(spacex_directory):
        print('''
        Spacex directory is not launched yet.
        Try to run fetch_spacex.py to get some new images!
        ''')
    else:
        post_photos_from_directory(spacex_directory, bot)

    hubble_directory = os.path.join(IMAGE_DIRECTORY_ROOT, HUBBLE_DIRECTORY_NAME)
    if not os.path.isdir(hubble_directory):
        print('''
        Hubble directory is not found.
        Try to run fetch_hubble.py to get some photo's from hubble telescope!
        ''')
    else:
        post_photos_from_directory(hubble_directory, bot)
