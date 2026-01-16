"""Enumerations for the game."""
from enum import Enum


class Weather(Enum):
    HOT = "hot"
    COLD = "cold"
    NICE = "nice"

    def is_harsh(self) -> bool:
        return self in (Weather.HOT, Weather.COLD)


class Strategy(Enum):
    SOFT = "Preach Softly"
    INTENSE = "Preach Intensely"


class Religion(Enum):
    EVANGELIST = "Evangelist"
    JEHOVAHS_WITNESS = "Jehovah's Witness"
    MORMON = "Mormon"
    CUSTOM = "Custom"
    SATANIC = "Satanic"


class LocationType(Enum):
    HOUSE = "House"
    STORE = "Store"
    CHURCH = "Church"
    LIBRARY = "Library"
