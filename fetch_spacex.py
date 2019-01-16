import requests
import sys

from common import (
    create_spacex_mission_directory,
    load_image_to_directory,
    build_image_name,
)


def get_spacex_last_launch_required_data():
    spacex_url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(spacex_url)
    try:
        json_response = response.json()
    except ValueError as e:
        return None, f'Cannot parse response from spacex: {e}'

    if not response.ok:
        error_message = 'Response status: {}, error message: {}'
        error_message = error_message.format(
            response.status_code,
            json_response.get('error'))
        return None, error_message

    mission_name = json_response.get('mission_name', None)
    if mission_name is None:
        return None, 'Response cannot be parsed properly: element mission_name not found.'

    links_object = json_response.get('links', None)
    if links_object is None:
        return None, 'Response cannot be parsed properly: element links not found.'

    images = links_object.get('flickr_images', None)
    if images is None:
        return None, 'Response cannot be parsed properly: element flickr_images not found.'

    required_data = {
        'mission_name': mission_name,
        'images': images
    }
    return required_data, ''


def fetch_spacex_last_launch_images():
    spacex_data, error_message = get_spacex_last_launch_required_data()

    if spacex_data is None:
        return None, error_message

    current_mission_directory, error_message = create_spacex_mission_directory(
        spacex_data.get('mission_name'))

    if current_mission_directory is None:
        return None, error_message

    images_urls = spacex_data.get('images')

    res = []

    for index, img_url in enumerate(images_urls):
        image_name = build_image_name(index + 1, img_url)

        saved_image_path = load_image_to_directory(
            current_mission_directory,
            image_name,
            img_url)

        if saved_image_path:
            res.append(saved_image_path)

    return res, ''


if __name__ == '__main__':
    saved_images, error_message = fetch_spacex_last_launch_images()
    if saved_images is None:
        sys.exit(error_message)
    print('Here saved images: {}'.format(saved_images))
