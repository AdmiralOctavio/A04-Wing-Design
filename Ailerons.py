import math
from math import pi
import numpy as np
import yaml

from isa import get_density
from mass_estimate import calculate_landing_mass
from utils import calculate_approach_speed
from wing_design import calculate_quarter_chord_sweep_angle, calculate_taper_ratio, \
    calculate_wing_span, calculate_root_chord, calculate_tip_chord


def calculate_aileron_control_derivative(start_y: float, end_y: float,
                                         airfoil_lift_curve_slope: float, aileron_effectiveness: float,
                                         wing_area: float, wing_span: float, tip_chord: float,
                                         root_chord: float) -> float:
    # From equation on ADSEE II Lecture 3 Slides page 57
    return ((2 * airfoil_lift_curve_slope * aileron_effectiveness) / (wing_area * wing_span) *
            ((2 / (3 * wing_span)) * (tip_chord - root_chord) * (end_y ** 3 - start_y ** 3) +
             (root_chord / 2) * (end_y ** 2 - start_y ** 2)))


def calculate_roll_damping_coefficient(wing_span: float, airfoil_lift_curve_slope: float,
                                       airfoil_zero_lift_drag_coefficient: float, wing_area: float,
                                       tip_chord: float, root_chord: float):
    # From equation on ADSEE II Lecture 3 Slides page 59
    return (-1 * (4 * wing_span / wing_area) * (airfoil_lift_curve_slope + airfoil_zero_lift_drag_coefficient) *
            (tip_chord / 32 + root_chord / 96))


def calculate_roll_rate(aileron_control_derivative: float, roll_damping_coefficient: float,
                        aileron_deflection: float, minimum_control_speed: float, wing_span: float) -> float:
    # From equation on ADSEE II Lecture 3 Slides page 60
    return (-1 * (aileron_control_derivative / roll_damping_coefficient) * aileron_deflection *
            (2 * minimum_control_speed / wing_span))


def main():
    # Load Parameters
    with open("aircraft_parameters.yaml") as file:
        aircraft_parameters = yaml.safe_load(file)

    requirements = aircraft_parameters["requirements"]
    wing_parameters = aircraft_parameters["wing"]
    aileron_parameters = wing_parameters["ailerons"]
    airfoil_parameters = wing_parameters["airfoil"]

    cruise_mach = requirements["cruise_mach"]  # [Mach]

    wing_area = wing_parameters["wing_area"]  # [m^2]
    aspect_ratio = aircraft_parameters["aspect_ratio"]  # [-]

    gravity = aircraft_parameters["gravity"]  # [m/s^2]

    quarter_chord_sweep_angle = calculate_quarter_chord_sweep_angle(
        cruise_mach)  # [m]
    taper_ratio = calculate_taper_ratio(quarter_chord_sweep_angle)  # [m]
    wing_span = calculate_wing_span(wing_area, aspect_ratio)  # [m]
    root_chord = calculate_root_chord(wing_area, taper_ratio, wing_span)  # [m]
    tip_chord = calculate_tip_chord(taper_ratio, root_chord)  # [m]

    deflection_angle_up = aileron_parameters["deflection_angle_up"]  # [deg]
    # [deg]
    deflection_angle_down = aileron_parameters["deflection_angle_down"]
    aileron_deflection = math.radians(
        0.5 * (deflection_angle_up + deflection_angle_down))  # [rad]

    airfoil_lift_curve_slope = (1.279 - 1.229) / math.radians(5)
    # [-]
    airfoil_zero_lift_drag_coefficient = airfoil_parameters["zero_lift_drag_coefficient"]
    aileron_effectiveness = aileron_parameters["aileron_effectiveness"]  # [-]

    landing_weight = calculate_landing_mass() * gravity  # [N]
    minimum_control_speed = calculate_approach_speed(
        landing_weight, get_density(0), wing_area)  # [m]

    roll_requirement = requirements["required_roll_rate"]
    required_roll_rate = math.radians(
        roll_requirement["degrees"]) / roll_requirement["seconds"]

    roll_damping_coefficient = calculate_roll_damping_coefficient(wing_span, airfoil_lift_curve_slope,
                                                                  airfoil_zero_lift_drag_coefficient, wing_area,
                                                                  tip_chord, root_chord)

    # [-]
    span_wise_ratio_lower_bound = aileron_parameters["span_wise_ratio_lower_bound"]
    # [-]
    span_wise_ratio_upper_bound = aileron_parameters["span_wise_ratio_upper_bound"]

    half_span = wing_span / 2  # [m]

    span_wise_position_lower_bound = span_wise_ratio_lower_bound * \
        half_span  # [m]
    span_wise_position_upper_bound = span_wise_ratio_upper_bound * \
        half_span  # [m]

    n = 1000  # [-]
    lower_bounds = np.linspace(
        span_wise_position_lower_bound, span_wise_position_upper_bound, n)  # [m]
    upper_bounds = np.linspace(
        span_wise_position_lower_bound, span_wise_position_upper_bound, n)  # [m]

    all_bounds = np.array(np.meshgrid(
        lower_bounds, upper_bounds)).T.reshape(-1, 2)
    valid_bound_bool_map = np.all(
        all_bounds[:, 1:] > all_bounds[:, :-1], axis=1)
    valid_bounds = all_bounds[valid_bound_bool_map]

    valid_design_options = []

    for lower_bound, upper_bound in valid_bounds:
        aileron_control_derivative = calculate_aileron_control_derivative(lower_bound, upper_bound,
                                                                          airfoil_lift_curve_slope,
                                                                          aileron_effectiveness, wing_area,
                                                                          wing_span,
                                                                          tip_chord, root_chord)

        roll_rate = calculate_roll_rate(aileron_control_derivative, roll_damping_coefficient, aileron_deflection,
                                        minimum_control_speed, wing_span)

        if roll_rate > required_roll_rate:
            valid_design_options.append((lower_bound, upper_bound))

    print(
        f"Out of {len(valid_bounds)} evaluated designs, {len(valid_design_options)} are valid.")

    minimum_span = math.inf
    for lower_bound, upper_bound in valid_design_options:
        span = upper_bound - lower_bound  # [m]

        if span < minimum_span:
            minimum_span = span

    minimum_span_designs = []

    for lower_bound, upper_bound in valid_design_options:
        span = upper_bound - lower_bound

        if span <= minimum_span:
            minimum_span_designs.append((lower_bound, upper_bound))

    print(
        f"Only {len(minimum_span_designs)} valid designs have the minimum aileron span of {minimum_span:.3f} [m].")
    print(f"These designs are:")

    for lower_bound, upper_bound in minimum_span_designs:
        print(f"b1 = {lower_bound:.5f} [m], b2 = {upper_bound:.5f} [m]")


if __name__ == '__main__':
    main()
