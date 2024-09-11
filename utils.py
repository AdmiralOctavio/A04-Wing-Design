import math
from enum import Enum

from isa import get_temperature


class FlightConfiguration(Enum):
    CRUISE = "cruise"
    TAKEOFF = "takeoff"
    LANDING = "landing"


def convert_square_meters_to_square_feet(square_meters: float) -> float:
    return square_meters * 10.76391  # [sq. ft]


def convert_feet_to_meters(feet: float) -> float:
    return feet * 0.3048  # [m]


def get_speed_of_sound(altitude: float) -> float:
    temperature = get_temperature(altitude)
    return math.sqrt(1.4 * 287 * temperature)
