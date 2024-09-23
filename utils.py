import math
from enum import Enum

import numpy as np


class FlightConfiguration(Enum):
    Cruise = "cruise"
    Takeoff = "takeoff"
    Landing = "landing"


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


def polygon_area(x_points, y_points):
    return 0.5 * np.abs(np.dot(x_points, np.roll(y_points, 1)) - np.dot(y_points, np.roll(x_points, 1)))


def lerp(a, b, t):
    return a + (b - a) * t
