import math
import yaml

from utils import FlightConfiguration

with open("aircraft_parameters.yaml") as file:
    aircraft_parameters = yaml.safe_load(file)

estimation_parameters = aircraft_parameters['zero_lift_drag_coefficient_estimation']

aspect_ratio = aircraft_parameters['aspect_ratio']  # [-]
wetted_to_reference_area_ratio = estimation_parameters['wetted_to_reference_area_ratio']  # [-]
equivalent_friction_coefficient = estimation_parameters['equivalent_friction_coefficient']  # [-]
span_efficiency = estimation_parameters['span_efficiency']  # [-]
lift_dependent_parasite_drag_parameter = estimation_parameters['lift_dependent_parasite_drag_parameter']  # [-]
flap_efficiency_penalty = estimation_parameters['flap_efficiency_penalty']  # [-]
flap_zero_lift_penalty = estimation_parameters['flap_zero_lift_penalty']  # [-]
gear_zero_lift_penalty = estimation_parameters['gear_zero_lift_penalty']  # [-]


def approximate_reference_wetted_area():
    # TODO: Calculate this directly from reference aircraft data
    average_ref_wing_area = 69.74  # [m2] From Excel WP1.2 (reference aircraft)

    return wetted_to_reference_area_ratio * average_ref_wing_area  # [m2]


def calculate_zero_lift_drag_coefficient(flight_configuration: FlightConfiguration, gear_extended: bool) -> float:
    base_coefficient = equivalent_friction_coefficient * wetted_to_reference_area_ratio

    flap_angle = aircraft_parameters['flap_angle'][flight_configuration.value]
    flap_penalty = flap_zero_lift_penalty * flap_angle

    gear_penalty = gear_zero_lift_penalty * gear_extended

    return base_coefficient + flap_penalty + gear_penalty


def calculate_oswald_efficiency_factor(flight_configuration: FlightConfiguration, gear_extended: bool):
    oswald_efficiency_factor = 1 / (
            math.pi * aspect_ratio * lift_dependent_parasite_drag_parameter + (1 / span_efficiency))

    flap_angle = aircraft_parameters['flap_angle'][flight_configuration.value]
    flap_penalty = flap_efficiency_penalty * flap_angle

    return oswald_efficiency_factor + flap_penalty


def main():
    print("{:<15} {:<10} {:<10} {:<10}".format("Flight Config.", "Gear", "e", "CD_0"))

    flight_configurations = [FlightConfiguration.CRUISE, FlightConfiguration.TAKEOFF, FlightConfiguration.LANDING]
    for flight_configuration in flight_configurations:
        for gear_down in [True, False]:
            oswald = calculate_oswald_efficiency_factor(flight_configuration, gear_down)
            coefficient = calculate_zero_lift_drag_coefficient(flight_configuration, gear_down)

            gear_down_string = "Gear Down" if gear_down else "Gear Up"

            print("{:<10} {:<10} {:>10.5f} {:>10.5f}".format(
                flight_configuration.value.title(),
                gear_down_string,
                oswald,
                coefficient
            ))


if __name__ == "__main__":
    main()
