""" import modules """
from abc import ABC, abstractmethod

from pydantic import BaseModel


class CompareLocationBody(BaseModel):
    """ compare location body """
    location_one: str
    location_two: str
    radius: int = 10


class LocationBody(BaseModel):
    """ location body """
    location: str


class ILocation(ABC):
    """ Location interface """
    @abstractmethod
    def normalize_location(self, location: str) -> dict:
        """ return all access key array """

    @abstractmethod
    def compare_location(self, payload: CompareLocationBody) -> bool:
        """ add new access key to the database """
