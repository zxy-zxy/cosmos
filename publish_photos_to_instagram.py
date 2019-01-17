import os
import sys

from dotenv import load_dotenv
from instabot import Bot

from utils.common import (
    get_hubble_directory,
    get_spacex_collection_directory
)
from utils.img_processing import fix_photo


def create_bot_instance():
    load_dotenv()
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

    bot = create_bot_instance()
    if bot is None:
        sys.exit('''
        Cannot log-in with provided credentials. 
        Check instagram_login and instagram_password env variables.
        ''')

    post_photos_from_directory(
        get_spacex_collection_directory(), bot)

    post_photos_from_directory(
        get_hubble_directory(), bot)
