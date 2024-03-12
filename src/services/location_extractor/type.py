from pydantic import BaseModel
import enum


class Geocode(str, enum.Enum):
    NOMINATION = "OPENMAP"
    GOOGLE = "GOOGLE"


class LocationBody(BaseModel):
    raw_text: str
    geocode: Geocode
