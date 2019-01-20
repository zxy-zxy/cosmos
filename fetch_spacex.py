import sys
import os

import requests

from utils.common import (
    IMAGE_DIRECTORY_ROOT,
    SPACEX_DIRECTORY_NAME,
    create_directory,
    load_image_to_directory,
    build_full_image_name
)
from utils.exceptions import (
    BadResponseException,
    RequiredFieldIsMissingException
)


def fetch_spacex_last_mission_data():
    spacex_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(spacex_url)
    try:
        json_response = response.json()
    except ValueError as e:
        raise BadResponseException(
            f'Cannot convert response from spacex to json: {e}'
        )

    if not response.ok:
        error_message = 'Response is not ok. Status: {}, error message: {}'
        error_message = error_message.format(
            response.status_code,
            json_response.get('error')
        )
        raise BadResponseException(error_message)

    try:
        mission_name = json_response['mission_name']
    except KeyError:
        raise RequiredFieldIsMissingException('mission_name')

    try:
        links_object = json_response['links']
    except KeyError:
        raise RequiredFieldIsMissingException('links')

    try:
        images = links_object['flickr_images']
    except KeyError:
        raise RequiredFieldIsMissingException('flickr_images')

    required_data = {
        'mission_name': mission_name,
        'imgs': images
    }

    return required_data


def fetch_spacex_last_mission_images(dir_name, imgs_urls):
    res = []

    for index, img_url in enumerate(imgs_urls):
        image_name = build_full_image_name(index + 1, img_url)

        saved_image_path = load_image_to_directory(
            dir_name,
            image_name,
            img_url
        )

        if saved_image_path:
            res.append(saved_image_path)

    return res


if __name__ == '__main__':
    try:
        spacex_last_mission_data = fetch_spacex_last_mission_data()
    except (BadResponseException, RequiredFieldIsMissingException) as e:
        sys.exit(e)

    mission_name = spacex_last_mission_data['mission_name']
    mission_imgs_urls = spacex_last_mission_data['imgs']

    try:
        mission_dir_name = os.path.join(
            IMAGE_DIRECTORY_ROOT,
            SPACEX_DIRECTORY_NAME,
            mission_name
        )
        create_directory(mission_dir_name)
    except OSError as e:
        sys.exit(f'Cannot created directory: {dir_name}. Error occured: {e}')

    saved_images = fetch_spacex_last_mission_images(
        mission_dir_name,
        mission_imgs_urls
    )

    print(f'Images has been fetched: {saved_images}')
