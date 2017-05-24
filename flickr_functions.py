"""Functions using Flickr API"""

import flickrapi
import json
import os

api_key = os.environ[u'FLICKR_KEY']
api_secret = os.environ[u'FLICKR_SECRET']

flickr = flickrapi.FlickrAPI(api_key, api_secret)

URL_TEMPLATE = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"


def get_photos(search, button):
    """Get URL for photo"""

    print "i am in " + button

    # using flickr api search method
    photos = flickr.photos.search(text=search, per_page="20", has_geo="1",
                                  format='json', tags=button, tag_mode='all',
                                  accuracy='16')
    # converts JSON string to dictionary
    photo_data = json.loads(photos)

    # filters results to prevent multiple results from one user
    # existing_users = set()

    # builds url by appending photo_id, user_id to pass into flickr url template
    image_urls = []
    for data in range(len(photo_data['photos']['photo'])):
        user_id = photo_data['photos']['photo'][data]['owner']
        # if user_id not in existing_users:
        photo_id = photo_data['photos']['photo'][data]['id']
        photo_source_template = "https://www.flickr.com/photos/{}/{}/"
        photo_source_url = photo_source_template.format(user_id, photo_id)

        farm_id = photo_data['photos']['photo'][data]['farm']
        server_id = photo_data['photos']['photo'][data]['server']
        photo_secret = photo_data['photos']['photo'][data]['secret']

        photo_url = URL_TEMPLATE.format(farm_id, server_id, photo_id, photo_secret)
        image_urls.append([photo_id, photo_source_url, photo_url])
        # existing_users.add(user_id)

    return image_urls


def get_url(photo_id):
    """Use photo_id to get link of photo to display on photo-info page"""

    # using flickr api get info method
    data = flickr.photos.getInfo(photo_id=photo_id, format='json')
    # converts JSON string to dictionary
    photo_data = json.loads(data)

    photo_id = photo_id
    farm_id = photo_data['photo']['farm']
    server_id = photo_data['photo']['server']
    photo_secret = photo_data['photo']['secret']

    photo_url = URL_TEMPLATE.format(farm_id, server_id, photo_id, photo_secret)

    return photo_url


def get_location(photo_id):
    """Get lat/lng of photo"""

    location_data = {}

    data = flickr.photos.geo.getLocation(photo_id=photo_id, format='json')
    location_info = json.loads(data)

    location_data['lat'] = location_info['photo']['location']['latitude']
    location_data['lng'] = location_info['photo']['location']['longitude']
    location_data['name'] = location_info['photo']['location']['locality']['_content']

    return location_data
