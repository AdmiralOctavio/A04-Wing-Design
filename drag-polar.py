import math

wet_to_ref_area_ratio = 6  # [-] From fig. 6.2 in ADSEE II airplane design reader

average_ref_wing_area = 69.74  # [m2] From Excel WP1.2 (reference aircraft)
approx_reference_wetted_areas = wet_to_ref_area_ratio * average_ref_wing_area  # [m2]


def convert_square_meters_to_square_feet(square_meters):
    return square_meters * 10.76391


print(str(convert_square_meters_to_square_feet(approx_reference_wetted_areas)) + " square feet wetted area")

equivalent_friction_coefficient = 0.0032  # [-] from fig. 6.3 in ADSEE II airplane design reader
zero_lift_drag_coefficient = equivalent_friction_coefficient * wet_to_ref_area_ratio  # [-]

print("CD_0 =", zero_lift_drag_coefficient)

aspect_ratio = 7.8  # [-]
span_efficiency = 0.97  # [-] from page 106 in ADSEE II
lift_dependent_parasite_drag_parameter = 0.0075  # [-] from page 106 in ADSEE II
oswald_efficiency_factor = 1 / (math.pi * aspect_ratio * lift_dependent_parasite_drag_parameter + (1 / span_efficiency))

print("e =", oswald_efficiency_factor)
