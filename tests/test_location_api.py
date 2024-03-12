""" all test modules """
import json
import unittest

from fastapi.testclient import TestClient

from src.routes.main import app


class LocationApiTesting(unittest.TestCase):
    """ unit test cases for location api """

    def setUp(self):
        """ setup function """
        self.app = TestClient(app)

        # Disable sending emails during unit testing
        # mail.init_app(app)

    def normalize_location(self, location):
        """ helps to make normalizeLocation call """
        return self.app.post('/v1/location/normalizeLocation',
                             data=json.dumps(location))

    def compare_location(self, location):
        """ helps to make compareLocation call """
        return self.app.post('/v1/location/compareLocation',
                             data=json.dumps(location))

    def test_input_normalize_location(self):
        """ test when no location given """
        response = self.normalize_location({})
        self.assertEqual(response.status_code, 422)

    def test__normalize_location(self):
        """ test when valid location given """
        response = self.normalize_location({"location": "kiet ghazibad"})
        self.assertEqual(response.status_code, 200)

    def test_input_one_compare_location(self):
        """ test when first location not given """
        response = self.compare_location({"location_two": "kiet ghaziabad"})
        self.assertEqual(response.status_code, 422)

    def test_input_two_compare_location(self):
        """ test when second location not given """
        response = self.compare_location({"location_one": "kiet ghazibad"})
        self.assertEqual(response.status_code, 422)

    def test_no_input_compare_location(self):
        """ test when no location given """
        response = self.compare_location({})
        self.assertEqual(response.status_code, 422)

    def test_compare_default_radius(self):
        """ test when valid location given """
        response = self.compare_location({"location_one": "kiet ghaziabad",
                                          "location_two": "adobe,noida"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data": {
                "isValidLocation": False
            },
            "error": None
        })

    def test_compare_on_radius(self):
        """ test when valid location and radius given """
        response = self.compare_location({"location_one": "kiet ghaziabad",
                                          "location_two": "adobe,noida",
                                          "radius": 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data": {
                "isValidLocation": True
            },
            "error": None
        })


if __name__ == "__main__":
    unittest.main()
