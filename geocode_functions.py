"""Using Google Maps Geocoding API."""

import googlemaps
import os

google_maps_api_key = os.environ['GOOGLE_KEY']

gmaps = googlemaps.Client(key=google_maps_api_key)


def reverse_geo_location(lat, lng):
    """Convert latitude and longitude to address using reverse geocode api method"""
    reverse_geo_result = gmaps.reverse_geocode((lat, lng))

    return reverse_geo_result[0]['formatted_address']
