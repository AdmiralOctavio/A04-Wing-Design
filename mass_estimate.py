import math

import yaml

from drag_polar import calculate_zero_lift_drag_coefficient, calculate_oswald_efficiency_factor
from utils import FlightConfiguration, convert_feet_to_meters, get_speed_of_sound


def calculate_lift_to_drag_ratio(
        flight_configuration: FlightConfiguration,
        gear_extended: bool,
        aspect_ratio: float
) -> float:
    zero_lift_drag_coefficient = calculate_zero_lift_drag_coefficient(flight_configuration, gear_extended)
    oswald_efficiency_factor = calculate_oswald_efficiency_factor(flight_configuration, gear_extended)
    return 0.5 * math.sqrt((math.pi * aspect_ratio * oswald_efficiency_factor)
                           / zero_lift_drag_coefficient)


def calculate_range_lost_due_to_drag(cruise_speed: float, cruise_altitude: float, aspect_ratio: float) -> float:
    cruise_lift_to_drag_ratio = calculate_lift_to_drag_ratio(FlightConfiguration.CRUISE, False, aspect_ratio)
    return ((1 / 0.7) * cruise_lift_to_drag_ratio *
            (cruise_altitude + math.pow(cruise_speed, 2) / (2 * 9.80665)))  # [m]


def calculate_thrust_specific_fuel_consumption(bypass_ratio: float) -> float:
    return 22 * math.pow(bypass_ratio, -0.19)  # [g/sec/kN]


def calculate_jet_efficiency(bypass_ratio: float, cruise_speed: float, fuel_specific_energy: float) -> float:
    thrust_specific_fuel_consumption = calculate_thrust_specific_fuel_consumption(bypass_ratio)
    return cruise_speed / (thrust_specific_fuel_consumption * fuel_specific_energy)


def calculate_equivalent_range(
        nominal_range: float,  # [m]
        divergence_range: float,  # [m]
        loiter_time: float,  # [secs]
        fuel_contingency_ratio: float,  # [-]
        cruise_speed: float,  # [m/s]
        cruise_altitude: float,  # [m]
        aspect_ratio: float,  # [-]
) -> float:
    lost_range = calculate_range_lost_due_to_drag(cruise_speed, cruise_altitude, aspect_ratio)
    return ((nominal_range + lost_range) * (1 + fuel_contingency_ratio) +
            1.2 * divergence_range + (loiter_time * cruise_speed))  # [m]


def calculate_class_i_estimation(
        nominal_range: float,  # [m]
        divergence_range: float,  # [m]
        loiter_time: float,  # [secs]
        fuel_contingency_ratio: float,  # [-]
        cruise_speed: float,  # [m/s]
        cruise_altitude: float,  # [m]
        bypass_ratio: float,  # [-]
        fuel_specific_energy: float,  # [MJ/kg]
        aspect_ratio: float,  # [-]
        design_payload: float,  # [kg]
) -> tuple[float, float, float, float]:
    equivalent_range = calculate_equivalent_range(nominal_range, divergence_range, loiter_time, fuel_contingency_ratio,
                                                  cruise_speed, cruise_altitude, aspect_ratio)  # [m]
    jet_efficiency = calculate_jet_efficiency(bypass_ratio, cruise_speed, fuel_specific_energy)
    lift_to_drag_ratio = calculate_lift_to_drag_ratio(FlightConfiguration.CRUISE, False, aspect_ratio)

    fuel_mass_fraction = 1 - math.exp(-equivalent_range / (1000000 * jet_efficiency * (fuel_specific_energy / 9.80665)
                                                           * lift_to_drag_ratio))
    operating_empty_mass_fraction = 0.566492308  # from ref. aircraft
    payload_mass_fraction = 1 - operating_empty_mass_fraction - fuel_mass_fraction

    mtow = design_payload / payload_mass_fraction
    fuel_mass = mtow * fuel_mass_fraction
    operating_empty_mass = mtow * operating_empty_mass_fraction
    landing_mass_fraction = 1 - nominal_range / equivalent_range * fuel_mass_fraction

    return mtow, fuel_mass, operating_empty_mass, landing_mass_fraction


def main():
    # Load Parameters
    with open("aircraft_parameters.yaml") as file:
        aircraft_parameters = yaml.safe_load(file)

    requirements = aircraft_parameters['requirements']
    engine_parameters = aircraft_parameters['engine']

    cruise_mach = requirements['cruise_mach']  # [Mach]
    cruise_altitude_feet = requirements['cruise_altitude']  # [feet]

    cruise_altitude = convert_feet_to_meters(cruise_altitude_feet)  # [m]
    speed_of_sound_at_cruise = get_speed_of_sound(cruise_altitude)  # [m/s]
    cruise_speed = cruise_mach * speed_of_sound_at_cruise  # [m/s]

    fuel_contingency_ratio = requirements['fuel_contingency_ratio']  # [-]
    diversion_range = requirements['diversion_range'] * 1000  # [m]
    nominal_range = requirements['nominal_range'] * 1000  # [m]
    loiter_time = requirements['loiter_time']  # [secs]

    design_payload = requirements['design_payload']  # [kg]

    design_bypass_ratio = engine_parameters['bypass_ratio']  # [-]
    specific_energy = engine_parameters['specific_energy']  # [MJ/kg]

    aspect_ratio = aircraft_parameters['aspect_ratio']  # [-]

    mtow_range = requirements['mtow_range'] * 1000  # [m]
    mtow_payload = requirements['mtow_payload']  # [kg]

    # Mission Profile 1: Design Range at Design Payload Mass
    profile1_mtow, profile1_fuel_mass, profile1_operating_empty_mass, profile1_landing_mass_fraction = (
        calculate_class_i_estimation(nominal_range, diversion_range, loiter_time, fuel_contingency_ratio,
                                     cruise_speed, cruise_altitude, design_bypass_ratio, specific_energy,
                                     aspect_ratio, design_payload))

    print(f"Profile 1: Design Range ({nominal_range / 1000:.0f} km) at Design Payload Mass ({design_payload} kg):")
    print(f"\tMTOW: {profile1_mtow} kg")
    print(f"\tFuel Mass: {profile1_fuel_mass} kg")
    print(f"\tOEM: {profile1_operating_empty_mass}")
    print(f"\tLanding Mass Fraction: {profile1_landing_mass_fraction}")

    print()

    # Mission Profile 2: MTOW Range at MTOW
    profile2_mtow, profile2_fuel_mass, profile2_operating_empty_mass, profile2_landing_mass_fraction = (
        calculate_class_i_estimation(mtow_range, diversion_range, loiter_time, fuel_contingency_ratio,
                                     cruise_speed, cruise_altitude, design_bypass_ratio, specific_energy,
                                     aspect_ratio, mtow_payload))

    print(f"Profile 2: Design Range ({mtow_range / 1000:.0f} km) at Design Payload Mass ({mtow_payload} kg):")
    print(f"\tMTOW: {profile2_mtow} kg")
    print(f"\tFuel Mass: {profile2_fuel_mass} kg")
    print(f"\tOEM: {profile2_operating_empty_mass}")
    print(f"\tLanding Mass Fraction: {profile2_landing_mass_fraction}")


if __name__ == "__main__":
    main()
