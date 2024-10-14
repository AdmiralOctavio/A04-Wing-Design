import math
from enum import Enum

import numpy as np


class FlightConfiguration(Enum):
    Cruise = "cruise"
    Takeoff = "takeoff"
    Landing = "landing"


class WingConfiguration(Enum):
    HighWing = 1
    LowWing = 2
    MidWing = 3


def convert_square_meters_to_square_feet(square_meters: float) -> float:
    return square_meters * 10.76391  # [sq. ft]


def convert_feet_to_meters(feet: float) -> float:
    return feet * 0.3048  # [m]


def load_airfoil_data(filename: str) -> tuple[list[float], list[float]]:
    with open(filename, "r") as file:
        points_x = []
        points_y = []

        lines = file.readlines()

        for line in lines[1:-1]:
            raw_points_str = line.split(" ")

            points_x.append(float(raw_points_str[0]))
            points_y.append(float(raw_points_str[1]))

        return points_x, points_y


def polygon_area(x_points: np.ndarray, y_points: np.ndarray) -> float:
    # From https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area#Python:_numpy
    i = np.arange(len(x_points))
    return np.abs(np.sum(x_points[i-1] * y_points[i] - x_points[i] * y_points[i-1]) * 0.5)


def lerp(a, b, t):
    return a + (b - a) * t


def calculate_approach_speed(weight: float, air_density: float, wing_area: float) -> float:
    stall_speed = calculate_stall_speed(weight, air_density, wing_area)
    return 1.23 * stall_speed


def calculate_stall_speed(weight: float, air_density: float, wing_area: float) -> float:
    maximum_lift_coefficient = calculate_maximum_lift_coefficient()

    return math.sqrt((2 * weight) / (air_density * wing_area * maximum_lift_coefficient))


def calculate_maximum_lift_coefficient(configuration: FlightConfiguration = FlightConfiguration.Landing) -> float:
    # TODO: These maximum lift coefficient values might change (?)
    if configuration == FlightConfiguration.Cruise:
        return 1.5
    elif configuration == FlightConfiguration.Landing:
        return 2.3
    elif configuration == FlightConfiguration.Takeoff:
        return 1.9
