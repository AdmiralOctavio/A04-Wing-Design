import math

import matplotlib.pyplot as plt
import numpy as np
import yaml

from mass_estimate import calculate_design_mtow, calculate_fuel_mass, calculate_operating_empty_mass, \
    calculate_design_equivalent_range, calculate_lift_to_drag_ratio, calculate_jet_efficiency
from utils import FlightConfiguration, convert_feet_to_meters, get_speed_of_sound

# Load Parameters
with open("aircraft_parameters.yaml") as file:
    aircraft_parameters = yaml.safe_load(file)

requirements = aircraft_parameters['requirements']
engine_parameters = aircraft_parameters['engine']

mtow = calculate_design_mtow()
fuel_mass = calculate_fuel_mass()
operating_empty_mass = calculate_operating_empty_mass()

mtow_payload = requirements['mtow_payload']
maximum_payload = requirements['maximum_payload']
design_payload = requirements['design_payload']

fuel_mass_structural_payload = mtow - operating_empty_mass - maximum_payload

equivalent_range = calculate_design_equivalent_range() / 1000  # [km]
nominal_range = requirements['nominal_range']  # [km]
auxiliary_range = equivalent_range - nominal_range
ferry_range = requirements['ferry_range']  # [km]
mtow_range = requirements['mtow_range']  # [km]

aspect_ratio = aircraft_parameters['aspect_ratio']
lift_to_drag_ratio = calculate_lift_to_drag_ratio(FlightConfiguration.Cruise, False, aspect_ratio)

cruise_mach = requirements['cruise_mach']  # [Mach]
cruise_altitude_feet = requirements['cruise_altitude']  # [feet]

cruise_altitude = convert_feet_to_meters(cruise_altitude_feet)  # [m]
speed_of_sound_at_cruise = get_speed_of_sound(cruise_altitude)  # [m/s]
cruise_speed = cruise_mach * speed_of_sound_at_cruise  # [m/s]

design_bypass_ratio = engine_parameters['bypass_ratio']  # [-]
specific_energy = engine_parameters['specific_energy']  # [MJ/kg]

jet_efficiency = calculate_jet_efficiency(design_bypass_ratio, cruise_speed, specific_energy)
gravity = aircraft_parameters['gravity']
specific_energy_joules = specific_energy * math.pow(10, 6)

range_at_maximum_structural_payload = (jet_efficiency * lift_to_drag_ratio * (specific_energy_joules / gravity) *
                                       math.log((operating_empty_mass + maximum_payload
                                                 + fuel_mass_structural_payload) / (operating_empty_mass +
                                                                                    maximum_payload)) - auxiliary_range)

fig, ax = plt.subplots()

points = np.array([
    (0, maximum_payload),
    (range_at_maximum_structural_payload / 1000, maximum_payload),
    (nominal_range, design_payload),
    (ferry_range, 0)
])
points_x, points_y = zip(*points)

ax.plot(points_x, points_y, marker="o")
ax.set_xlabel("Range [km]")
ax.set_ylabel("Payload Mass [kg]")

plt.grid(linestyle="dashed")
plt.show()

