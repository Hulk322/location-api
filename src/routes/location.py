""" import modules """
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..services.location.index import LocationManager
from ..services.location.type import CompareLocationBody, LocationBody

location_router = APIRouter()


@location_router.post('/normalizeLocation')
async def normalize_location(input_location: LocationBody):
    """ normalize input location """
    try:
        location_object = LocationManager()
        output_location = location_object.normalize_location(
            input_location.location)
        create_res = {
            "data": output_location,
            "error": None
        }
        return create_res
        # return {}
    except Exception as err:
        print('Error while normalizing location error : \
                {}'.format(err))
        return JSONResponse(status_code=400,
                            content={"data": None,
                                     "error":
                                     'Error while normalizing location'
                                     })


@location_router.post('/compareLocation')
async def compare_location(input_data: CompareLocationBody):
    """ compare input location and return
    true or false based on radius value """
    try:
        #location_object = LocationManager()
        #is_valid_location = location_object.compare_location(input_data)
        #create_res = {
        #    "data": {
        #        "isValidLocation": is_valid_location
        #    },
        #    "error": None
        #}
        return []#create_res
    except Exception as err:
        print('Error while comparing location error : \
                {}'.format(err))
        return JSONResponse(status_code=400,
                            content={"data": None,
                                     "error":
                                     'Error while comparing location'
                                     })


@location_router.post('/distance')
async def distance_bw_location(input_data: CompareLocationBody):
    """ compare input location and return
    true or false based on radius value """
    try:
        #location_object = LocationManager()
        #distance = location_object.distance_bw_location(input_data)
        #create_res = {
        #    "data": {
        #        "distance": distance,
        #        "measurement_unit": "KM"
        #    },
        #    "error": None
        #}
        return []#create_res
    except Exception as err:
        print('Error while calculating distance error : \
                {}'.format(err))
        return JSONResponse(status_code=400,
                            content={"data": None,
                                     "error":
                                     'Error while calculating distance'
                                     })
