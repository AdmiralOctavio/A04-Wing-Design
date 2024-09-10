from enum import Enum


def convert_square_meters_to_square_feet(square_meters):
    return square_meters * 10.76391


class FlightConfiguration(Enum):
    CRUISE = "cruise"
    TAKEOFF = "takeoff"
    LANDING = "landing"

def jetEfficiency(B):
    TSFC = 22 * B**(-.19)
    return Vcr/TSFC/ef
