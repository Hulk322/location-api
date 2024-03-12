import re
import requests
from urllib import parse
from src.config.config import settings
from src.utility.spacy_prediction import SpacyPrediction
import logging
from geopy.geocoders import Nominatim

settings = settings[settings.env]

class LocationService:

    def __init__(self) -> None:
        self.raw_list: list = []
        self.gpe_data: list = []
        self.google_api: str = f"https://maps.googleapis.com/maps/api/geocode/json?key={settings.api_key.google_api_key}&address="
        self.openstreet_api: str = ""
        self.geolocator = Nominatim(user_agent="geoapiExercises")

    def __clean_raw_text(self, raw_text: str) -> None:
        raw_text = raw_text.strip()
        raw_text = re.sub(r'\n', ' ', raw_text).strip()
        raw_text = re.sub(r' +', r' ', raw_text).strip()
        raw_data: list = raw_text.split(" ")
        i: int = 0
        while (i < len(raw_data)):
            if i+5 < len(raw_data):
                self.raw_list.append(" ".join(raw_data[i:i+5]).strip())
            else:
                self.raw_list.append(" ".join(raw_data[i:]).strip())
            i += 5

    def __get_prediction(self) -> list:
        raw_length: int = 0
        gpe_data: list = []
        for index, value in enumerate(self.raw_list, start=0):
            gpe_data = SpacyPrediction.gpe_prediction(value)
            if gpe_data == []:
                raw_length += len(value)+1
            else:
                gpe_data = [{"text": value.get('text'), "start_index": value.get(
                    'start_index')+raw_length} for value in gpe_data]
                raw_length += len(value)+1
                return gpe_data, index
        return {}, -1

    def __get_gpe_str(self, gpe_data: list) -> str:
        gpe_atr: list = []
        for gpe in gpe_data:
            gpe_atr.append(gpe.get("text"))
        return ", ".join(gpe_atr)

    def __select_data(self, index: int) -> str:
        raw_text: str = ""
        if index == -1:
            return " ".join(self.raw_list)
        elif index == 0:
            if index+2 <= len(self.raw_list)-1:
                raw_text = " ".join(self.raw_list[index:index+3])
            elif index+1 <= len(self.raw_list)-1:
                raw_text = " ".join(self.raw_list[index:index+2])
            else:
                raw_text = " ".join(self.raw_list[index:])
        elif index-1 >= 0:
            if index+2 <= len(self.raw_list)-1:
                raw_text = " ".join(self.raw_list[index-1:index+2])
            elif index+1 <= len(self.raw_list)-1:
                raw_text = " ".join(self.raw_list[index-1:index+1])
            else:
                raw_text = " ".join(self.raw_list[index-1:])
        return raw_text

    # def simp_prediction(self, elements):
    #     raw_length: int = 0
    #     gpe_data: list = []
    #     for index, value in enumerate(elements, start=0):
    #         print("value--------> ", value)
    #         gpe_data = SpacyPrediction.gpe_prediction(value)
    #         print("gpe_data ---------. ", gpe_data)
    #         if gpe_data == []:
    #             raw_length += len(value)+1
    #         else:
    #             gpe_data = [{"text": value.get('text'), "start_index": value.get(
    #                 'start_index')+raw_length} for value in gpe_data]
    #             raw_length += len(value)+1
    #             return gpe_data, index
    #     return {}, -1
    

    def simp_geocode(self, raw_text: str) -> dict:
        try:
            self.__clean_raw_text(raw_text.encode("ascii", "ignore").decode())
            gpe_data, index = self.__get_prediction()
            raw_text = self.__select_data(index)
            if gpe_data:
                location: dict = {}
                location["ner_address"] = self.__get_gpe_str(gpe_data)
                full_location = self.geolocator.geocode(location["ner_address"])
                if full_location:
                    address = (full_location.raw).get("display_name")
                else:
                    address = location["ner_address"]
                logging.warning(f"address ------> {address}")
                address = self.geopy_location(ladd1=address)
                location["formatted_address"] = {}
                location["formatted_address"]["address"] = raw_text
                location["formatted_address"]["state"] = address[1]
                location["formatted_address"]["country"] = address[2]
                location["formatted_address"]["city/district/county"] = address[0]
                return location
        except Exception as err:
            logging.warning(str(err))
            
    def google_geocode(self, raw_text: str) -> dict:
        try:
            self.__clean_raw_text(raw_text.encode("ascii", "ignore").decode())
            gpe_data, index = self.__get_prediction()
            raw_text = self.__select_data(index)
            data: dict = {}
            if gpe_data:
                data: dict = requests.get(
                    f"{self.google_api}{parse.quote(raw_text)}").json()
            location: dict = {}
            if data.get("status") == "OK":
                location["formatted_address"] = {}
                location["formatted_address"]["address"] = data.get(
                    "results")[0].get("formatted_address")
                for component in data["results"][0]["address_components"]:
                    if "country" in component["types"]:
                        location["formatted_address"]["country"] = \
                            component["long_name"]
                    if "administrative_area_level_1" in component["types"]:
                        location["formatted_address"]["state"] = \
                            component["long_name"]
                    if "administrative_area_level_2" in component["types"]:
                        location["formatted_address"]["city/district/county"] = component["long_name"]
            if gpe_data:
                location["ner_address"] = self.__get_gpe_str(gpe_data)

            return location
        except Exception as err:
            ...

    def open_map_geocode(self, raw_text: str) -> dict:
        try:
            self.__clean_raw_text(raw_text)
            gpe_data, index = self.__get_prediction()
            raw_text = self.__select_data(index)
            data: dict = requests.get(parse.quote(
                f"{self.openstreet_api}{raw_text}")).json()
            return data
        except Exception as err:
            if gpe_data:
                return self.__get_gpe_str(gpe_data)

    def city_state_country(self, coord):
        location = self.geolocator.reverse(coord, exactly_one=True)
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        return city, state, country
    
    
    def geopy_location(self, ladd1):
        location = self.geolocator.geocode(ladd1)
        if location:
            coord = f"{location.latitude}, {location.longitude}"
            address = self.city_state_country(coord)
            return address
        else:
            return ('', '', '')