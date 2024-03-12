""" import modules """
import googlemaps
from geopy.distance import distance

from src.config.config import settings
from .type import CompareLocationBody, ILocation
settings = settings[settings.env]

# function calculate distance between give latitude and longitude (KM)
def _distance_between_lat_and_long(lat_one: float,
                                   long_one: float,
                                   lat_two: float,
                                   long_two: float):
    """ distance between two location """
    try:
        return distance((lat_one, long_one), (lat_two, long_two)).km
    except Exception as err:
        print('Error while calculating distance error : \
            {}'.format(err))
        raise Exception('Error while calculating distance')


class LocationManager(ILocation):
    """ Location manager """

    def __init__(self):
        """ location  constructor"""
        self.gmaps = googlemaps.Client(
            key=settings.api_key.google_api_key)
        self.data_mapping = {
            "postal_code": "zipcode",
            "country": "country",
            "locality": "city",
            "administrative_area_level_1": "state"
        }

    def normalize_location(self, location: str):
        """ return normalize location """
        try:
            location_detail = self.gmaps.geocode(location)
            location_data = {}
            if location_detail:
                location_data["formatted_address"] = \
                    location_detail[0]["formatted_address"]
                location_data["geometry"] = {
                    "lat": location_detail[0]["geometry"]["location"]["lat"],
                    "lng": location_detail[0]["geometry"]["location"]["lng"]
                }

                for address in location_detail[0]["address_components"]:
                    if"postal_code" in address["types"]:
                        location_data[self.data_mapping["postal_code"]
                                    ] = address["long_name"]
                    if"country" in address["types"]:
                        if address.get("long_name"):
                            location_data[self.data_mapping["country"]] =\
                                address["long_name"]
                        if address.get("short_name"):
                            location_data["country_code"] = address["short_name"]
                    if"locality" in address["types"]:
                        if address.get("long_name"):
                            location_data[self.data_mapping["locality"]] =\
                                address["long_name"]
                        if address.get("short_name"):
                            location_data["city_code"] = address["short_name"]
                    if"administrative_area_level_1" in address["types"]:
                        if address.get("long_name"):
                            location_data[self.data_mapping["administrative_area_level_1"]] =\
                                address["long_name"]
                        if address.get("short_name"):
                            location_data["state_code"] = address["short_name"]
            return location_data
        except Exception as err:
            print('Error while normalizing location error : \
                {}'.format(err))
            raise Exception('Error while normalizing location')

    def compare_location(self, payload: CompareLocationBody):
        """ return bool value based on given radius """
        try:
            if payload.radius < self.distance_bw_location(payload):
                return False
            return True
        except Exception as err:
            print('Error while comparing location error : \
                {}'.format(err))
            raise Exception('Error while comparing location')

    def distance_bw_location(self, payload: CompareLocationBody):
        """ return bool value based on given radius """
        try:
            normalize_location_one = self.normalize_location(
                payload.location_one)
            normalize_location_two = self.normalize_location(
                payload.location_two)
            lat_one = normalize_location_one["geometry"]["lat"]
            lng_one = normalize_location_one["geometry"]["lng"]
            lat_two = normalize_location_two["geometry"]["lat"]
            lng_two = normalize_location_two["geometry"]["lng"]
            return _distance_between_lat_and_long(lat_one,
                                                  lng_one,
                                                  lat_two,
                                                  lng_two)
        except Exception as err:
            print('Error while calculating distance error : \
                {}'.format(err))
            raise Exception('Error while calculating distance')
