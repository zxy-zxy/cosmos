import os
from itertools import count

import requests

from utils.common import (
    IMAGE_DIRECTORY_ROOT,
    HUBBLE_DIRECTORY_NAME,
    load_image_to_directory,
    create_directory,
    build_full_image_name
)


def load_imgs_files(dir_name, imgs_files_to_load, limit=None):
    saved_images = []

    if limit is not None:
        imgs_files_to_load = imgs_files_to_load[:limit]

    for image in imgs_files_to_load:

        img_name = build_full_image_name(
            image['img_id'], image['img_file_url']
        )

        saved_image_path = load_image_to_directory(
            dir_name,
            img_name,
            image['img_file_url']
        )

        if saved_image_path:
            saved_images.append(saved_image_path)

    return saved_images


def get_img_file_url(img_id):
    image_url = f'http://hubblesite.org/api/v3/image/{img_id}'
    response = requests.get(image_url)

    if not response.ok:
        return None
    try:
        json_response = response.json()
    except ValueError:
        return None

    image_files_object = json_response.get('image_files', None)

    if image_files_object is None:
        return None

    return image_files_object[-1]['file_url']


def get_imgs_urls_to_download(imgs_ids, limit=None):
    images = []

    if limit is not None:
        imgs_ids = imgs_ids[:limit]

    for img_id in imgs_ids:

        image_file_url = get_img_file_url(img_id)

        if image_file_url is None:
            continue

        images.append({
            'img_id': img_id,
            'img_file_url': image_file_url}
        )

    return images


def parse_imgs_collection_response(response):
    if not response.ok:
        return None
    try:
        json_response = response.json()
    except ValueError:
        return None
    return [img_element['id'] for img_element in json_response]


def get_imgs_ids_from_collection(collection_name, page_limit=5):
    hubble_images_collection_url = f'http://hubblesite.org/api/' \
                                   f'v3/images/{collection_name}'
    images_ids = []
    for i in count(1):

        if i > page_limit:
            break

        response = requests.get(hubble_images_collection_url, params={'page': i})
        images_ids_from_page = parse_imgs_collection_response(response)

        if not images_ids_from_page:
            break

        images_ids.extend(images_ids_from_page)

    return images_ids


def fetch_hubble_images_from_collection(collection_name, collection_dir_name):
    imgs_id = get_imgs_ids_from_collection(
        collection_name,
    )

    imgs_urls_to_download = get_imgs_urls_to_download(
        imgs_id)

    fetched_images = load_imgs_files(
        collection_dir_name,
        imgs_urls_to_download,
    )

    return fetched_images


def get_available_collections():
    return [
        'holiday_cards',
        # 'wallpaper',
        # 'printshop',
        # 'stsci_gallery',
    ]


def fetch_hubble_images():
    available_collections = get_available_collections()
    for collection_name in available_collections:

        try:
            collection_dir_name = os.path.join(
                IMAGE_DIRECTORY_ROOT,
                HUBBLE_DIRECTORY_NAME,
                collection_name
            )
            create_directory(collection_dir_name)
        except OSError as e:
            print(f'Cannot created directory: {collection_name}. '
                  f'Error occured: {e}')
            continue

        saved_images = fetch_hubble_images_from_collection(
            collection_name, collection_dir_name
        )

        yield saved_images


if __name__ == '__main__':
    fetched_hubble_images = fetch_hubble_images()
    for saved_images in fetched_hubble_images:
        print('Here saved images: ')
        for saved_image in saved_images:
            print(saved_image)
