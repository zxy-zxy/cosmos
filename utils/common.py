import os
import errno
import requests

IMAGE_DIRECTORY_ROOT = 'images'
SPACEX_DIRECTORY_NAME = 'spacex'
HUBBLE_DIRECTORY_NAME = 'hubble'


def build_full_image_name(img_name, img_url):
    img_url_without_extension, img_extension = os.path.splitext(img_url)
    return f'{img_name}{img_extension}'


def load_image_to_directory(directory, image_name, image_url):
    image_path = os.path.join(directory, str(image_name))
    response = requests.get(image_url)
    if not response.ok:
        return None
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path


def create_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_spacex_mission_directory(mission_name):
    try:
        dir_name = os.path.join(
            IMAGE_DIRECTORY_ROOT,
            SPACEX_DIRECTORY_NAME,
            mission_name
        )
        create_directory(dir_name)
        return dir_name, ''
    except OSError as e:
        error_message = 'Cannot create directory {}. Error occured: {}'
        error_message = error_message.format(dir_name, e)
        return None, error_message


def get_spacex_collection_directory():
    return os.path.join(IMAGE_DIRECTORY_ROOT, SPACEX_DIRECTORY_NAME)


def create_hubble_collection_directory(hubble_collection_name):
    try:
        dir_name = os.path.join(
            IMAGE_DIRECTORY_ROOT,
            HUBBLE_DIRECTORY_NAME,
            hubble_collection_name
        )
        create_directory(dir_name)
        return dir_name, ''
    except OSError as e:
        error_message = 'Cannot create directory {}. Error occured: {}'
        error_message = error_message.format(dir_name, e)
        return None, error_message


def get_hubble_directory():
    return os.path.join(IMAGE_DIRECTORY_ROOT, HUBBLE_DIRECTORY_NAME)
