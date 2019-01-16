from itertools import count

import requests

from common import (
    load_image_to_directory,
    create_hubble_collection_directory,
    build_image_name
)


def load_imgs_files(collection_name, imgs_files_to_load, limit=None):
    hubble_collection_img_dir, error_message = create_hubble_collection_directory(
        collection_name)

    if hubble_collection_img_dir is None:
        return None, error_message

    saved_images = []

    if limit is None:
        limit = len(imgs_files_to_load)
    else:
        limit = min(len(imgs_files_to_load), limit)

    for image in imgs_files_to_load[:limit]:

        img_name = build_image_name(
            image['img_id'], image['img_file_url'])

        saved_image_path = load_image_to_directory(
            hubble_collection_img_dir,
            img_name,
            image['img_file_url'])

        if saved_image_path:
            saved_images.append(saved_image_path)

    return saved_images, ''


def parse_image_response(response):
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


def get_images_files_urls(imgs_ids, limit=None):
    images = []

    if limit is None:
        limit = len(imgs_ids)
    else:
        limit = min(len(imgs_ids), limit)

    for img_id in imgs_ids[:limit]:
        image_url = f'http://hubblesite.org/api/v3/image/{img_id}'
        response = requests.get(image_url)
        image_file_url = parse_image_response(response)

        if image_file_url is None:
            continue

        images.append({
            'img_id': img_id,
            'img_file_url': image_file_url}
        )

    return images


def parse_images_collection_response(response):
    if not response.ok:
        return None
    try:
        json_response = response.json()
    except ValueError:
        return None
    return [img_element['id'] for img_element in json_response]


def get_images_ids_from_collection_pages(collection_name, page_limit=5):
    hubble_images_collection_url = f'http://hubblesite.org/api/v3/images/{collection_name}'
    images_ids = []
    for i in count(1):

        if i > page_limit:
            break

        response = requests.get(hubble_images_collection_url, params={'page': i})
        images_ids_from_page = parse_images_collection_response(response)

        if not images_ids_from_page:
            break

        images_ids.extend(images_ids_from_page)

    return images_ids


def fetch_hubble_images_from_collection(collection_name):
    images_per_collection_limit = None

    imgs_ids = get_images_ids_from_collection_pages(
        collection_name)

    imgs_files_to_load = get_images_files_urls(
        imgs_ids,
        images_per_collection_limit)

    fetched_images, error = load_imgs_files(
        collection_name,
        imgs_files_to_load,
        images_per_collection_limit)

    return fetched_images, error


def get_available_collections():
    return [
        'holiday_cards',
        'wallpaper',
        'printshop',
        'stsci_gallery',
    ]


def fetch_hubble_images():
    available_collections = get_available_collections()
    for collection_name in available_collections:
        saved_images, error = fetch_hubble_images_from_collection(collection_name)
        yield (saved_images, error)


if __name__ == '__main__':
    fetched_hubble_images = fetch_hubble_images()
    for saved_images, error in fetched_hubble_images:
        if error:
            print(f'Error has occured: {error}')
        else:
            print('Here saved images: ')
            for saved_image in saved_images:
                print(saved_image)
