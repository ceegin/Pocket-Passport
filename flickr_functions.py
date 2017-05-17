"""Functions for Flickr API requests."""

import flickrapi
import json
import os

api_key = os.environ[u'FLICKR_KEY']
api_secret = os.environ[u'FLICKR_SECRET']

flickr = flickrapi.FlickrAPI(api_key, api_secret)


def get_photos(search, button):
    """Get URL for photo"""
    image_urls = []

    print "i am in " + button

    photos = flickr.photos.search(text=search, per_page='12', format='json', tags=button, tag_mode='all')

    photo_data = json.loads(photos)

    for data in range(len(photo_data['photos']['photo'])):
        photo_id = photo_data['photos']['photo'][data]['id']
        user_id = photo_data['photos']['photo'][data]['owner']
        photo_source_template = "https://www.flickr.com/photos/{}/{}/"
        photo_source_url = photo_source_template.format(user_id, photo_id)

        farm_id = photo_data['photos']['photo'][data]['farm']
        server_id = photo_data['photos']['photo'][data]['server']
        photo_secret = photo_data['photos']['photo'][data]['secret']

        photo_url_template = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"
        photo_url = photo_url_template.format(farm_id, server_id, photo_id, photo_secret)
        image_urls.append([photo_id, photo_source_url, photo_url])

    return image_urls


