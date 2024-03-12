""" Location api to extract location from raw text """
from fastapi import APIRouter
from ..services.location_extractor.index import LocationService
from ..services.location_extractor.type import LocationBody, Geocode
import time

location_extractor_route = APIRouter()


@location_extractor_route.post('/v1/extract-location')
def extract_location(payload: LocationBody):
    """ routes help's to extract location from raw text """
    start: int = time.time()
    location_obj: LocationService = LocationService()
    if payload.geocode.value == Geocode.GOOGLE:
        location: dict = location_obj.google_geocode(payload.raw_text)
    if payload.geocode.value == Geocode.NOMINATION:
        location: dict = location_obj.simp_geocode(payload.raw_text)
    end: int = time.time()
    return {
        "data": {
            "location": location,
            "total_time": end - start
        },
        "error": None
    }
@location_extractor_route.get('/health-check', include_in_schema=False)
async def check_server():
    """ help to check server is live or not """
    response = {"info": "Location API is started"}
    return response
