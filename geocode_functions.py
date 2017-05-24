"""Using Google Maps Geocoding API."""

import googlemaps
import os

google_maps_api_key = os.environ['GOOGLE_KEY']

gmaps = googlemaps.Client(key=google_maps_api_key)


def geo_code_location(city):
    """Convert the address of a city to its latitude and longitude points."""

    # using geocode api method to get lat/lng
    geocode_result = gmaps.geocode(city)

    # if no geocode provided
    if geocode_result == []:
        return None

    # gets latitude and longitude points
    return (geocode_result[0]['geometry']['location']['lat'],
            geocode_result[0]['geometry']['location']['lng']
            )


def reverse_geo_location(lat, lng):
    """Convert latitude and longitude to address using reverse geocode api method"""
    # using reverse geocode api method to get formatted address
    reverse_geo_result = gmaps.reverse_geocode((lat, lng))

    return reverse_geo_result[0]['formatted_address']
