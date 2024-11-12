import math

import matplotlib.pyplot as plt
import numpy as np
import shapely

tire_pressure = 782000  # [Pa] TODO: When static load changes, this must be retrieved from the graph again
tip_over_angle = 12  # [deg]
scrape_angle = 8  # [deg]
overturn_angle = 55  # [deg]
ground_clearance_angle = 5  # [deg]
compression_stroke = 0.3  # [m]
vertical_cg_fraction = 0.6  # [-] TODO: what the fuck

# Aircraft parameters
MTOW = 23173.027059606364 # [kg]
wing_span = 23.295063854816966  # [m]
dihedral_angle = -0.3504328752335939  # [deg]
engine_diameter = 1.08  # [m]
engine_wing_position = 0.35 * wing_span / 2  # [m]
x_cg_pos = 14.2 # [m] from nose

# Fuselage Dimensions
fuselage_diameter = 2.904633871690015  # [m]
cabin_length = 19.44  # [m]
nose_cone_length = 1.8 * fuselage_diameter  # [m]
tail_cone_length = 2.5 * fuselage_diameter  # [m]

# Wing Dimensions


cg_position = shapely.Point(x_cg_pos, vertical_cg_fraction * fuselage_diameter)


def convert_inches_to_meters(inches):
    return inches * 0.0254


def get_angle_contraint_line_from_angle_and_point(point: shapely.Point, angle: float,
                                                  length: float) -> shapely.LineString:
    angle_rad = math.radians(angle)
    line_offset = np.array([length * math.cos(angle_rad), length * math.sin(angle_rad)])

    start = np.array(*point.coords) - line_offset
    end = np.array(*point.coords) + line_offset

    return shapely.LineString([start, end])


if not tip_over_angle > scrape_angle:
    raise AssertionError("The tip over angle must be greater than the scrape angle!")

diameter_main = convert_inches_to_meters(33)  # [m] MUST BE CHANGED IF CHANGING PRESSURE (FROM GRAPHS)
diameter_nose = convert_inches_to_meters(18)  # [m] MUST BE CHANGED IF CHANGING PRESSURE (FROM GRAPHS)

width_main = convert_inches_to_meters(9.75)  # [m] MUST BE CHANGED IF CHANGING PRESSURE (FROM GRAPHS)
width_nose = convert_inches_to_meters(4.25)  # [m] MUST BE CHANGED IF CHANGING PRESSURE (FROM GRAPHS)

print(f"main tire diameter: {diameter_main} m")

aircraft_weight = MTOW * 9.80665  # [N]

n_main_wheels = max(4 * round(aircraft_weight / (120000 * 4)), 4)
n_nose_wheels = 2

static_load_main = 0.92 * aircraft_weight / n_main_wheels  # [N] per tire
static_load_nose = 0.08 * aircraft_weight / n_nose_wheels  # [N] per tire

print(f"{n_main_wheels = }")
print(f"{static_load_main = }")
print(f"{static_load_nose = }")

# FUSELAGE GEOMETRY
nose_cone_point = shapely.Point(0, 0)
cabin_top_left = shapely.Point(nose_cone_length, fuselage_diameter)
tail_cone_point = shapely.Point(nose_cone_length + cabin_length + tail_cone_length, fuselage_diameter)
cabin_bottom_right = shapely.Point(nose_cone_length + cabin_length, 0)
cabin_bottom_left = shapely.Point(nose_cone_length, 0)

fuselage_polygon = shapely.Polygon([
    nose_cone_point, cabin_top_left, tail_cone_point, cabin_bottom_right, cabin_bottom_left
])

adapated_scrape_position = shapely.Point(
    nose_cone_length + cabin_length - 0.5 * diameter_main * math.cos(math.radians(scrape_angle)),
    0.5 * diameter_main * math.sin(math.radians(scrape_angle)) - compression_stroke,
)

scrape_constraint = get_angle_contraint_line_from_angle_and_point(adapated_scrape_position, scrape_angle, 10)
original_scrape_constraint = get_angle_contraint_line_from_angle_and_point(cabin_bottom_right, scrape_angle, 10)
tip_over_constraint = get_angle_contraint_line_from_angle_and_point(cg_position, 90 + tip_over_angle, 10)

main_gear_position = scrape_constraint.intersection(tip_over_constraint)
main_gear_wheel = main_gear_position.buffer(diameter_main * 0.5)

main_gear_relative_position = main_gear_position.x - cg_position.x

# Pn * ln = Pm * lm
# ln = Pm * lm / Pn
nose_gear_relative_position = (static_load_main * n_main_wheels * main_gear_relative_position) / (
            static_load_nose * n_nose_wheels)
print(nose_gear_relative_position)

nose_gear_position = shapely.Point(cg_position.x - nose_gear_relative_position,
                                   main_gear_position.y - 0.5 * (diameter_main - diameter_nose))
nose_gear_wheel = nose_gear_position.buffer(diameter_nose * 0.5)

compressed_main_wheel = shapely.Point(
    main_gear_position.x, main_gear_position.y + compression_stroke
).buffer(diameter_main * 0.5)

floor_line = shapely.LineString([
    shapely.Point(0, main_gear_position.y - diameter_main * 0.5),
    shapely.Point(32, nose_gear_position.y - diameter_nose * 0.5),
])

front_fuselage = shapely.Point(0, fuselage_diameter / 2).buffer(fuselage_diameter / 2)

# WING GEOMETRY
tip_z_position = fuselage_diameter + 0.5 * wing_span * math.sin(math.radians(dihedral_angle))
floor_to_tip_distance = abs(tip_z_position - (main_gear_position.y - diameter_main * 0.5))

wing_line = shapely.LineString([
    shapely.Point(wing_span / 2, tip_z_position),
    shapely.Point(0, fuselage_diameter),
    shapely.Point(-wing_span / 2, tip_z_position),
])

left_engine_position = shapely.Point(
    -engine_wing_position,
    fuselage_diameter + engine_wing_position * math.sin(math.radians(dihedral_angle)) - engine_diameter / 2
)

right_engine_position = shapely.Point(
    engine_wing_position,
    fuselage_diameter + engine_wing_position * math.sin(math.radians(dihedral_angle)) - engine_diameter / 2
)

left_engine = left_engine_position.buffer(engine_diameter / 2)
right_engine = right_engine_position.buffer(engine_diameter / 2)

fuselage_distance_to_floor = abs(main_gear_position.y - diameter_main * 0.5)
engine_to_floor_distance = right_engine_position.y - engine_diameter / 2 + fuselage_distance_to_floor

lateral_tipover_criterion = (nose_gear_relative_position + main_gear_relative_position) / math.sqrt(
    math.pow(
        (nose_gear_relative_position * math.tan(math.radians(overturn_angle)))
        / (cg_position.y + fuselage_distance_to_floor),
        2) - 1
)

lateral_tip_ground_clearance_criterion = (wing_span / 2) - (
            floor_to_tip_distance / math.tan(math.radians(ground_clearance_angle)))
lateral_engine_ground_clearance_criterion = (wing_span / 2) - (
            engine_to_floor_distance / math.tan(math.radians(ground_clearance_angle)))

wheel_lateral_offset = max(lateral_tipover_criterion, lateral_engine_ground_clearance_criterion,
                           lateral_tip_ground_clearance_criterion)

left_wheels = shapely.box(wheel_lateral_offset - (n_main_wheels / 2) * width_main / 2,
                          -fuselage_distance_to_floor,
                          wheel_lateral_offset + (n_main_wheels / 2) * width_main / 2,
                          diameter_main - fuselage_distance_to_floor)

print(f"{wheel_lateral_offset = } m")

print(f"Main Gear Position wrt. tip of nose and bottom of fuselage: {main_gear_position}")

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.set_aspect(1)

ax1.plot(*fuselage_polygon.exterior.xy)
ax1.plot(*original_scrape_constraint.xy)
ax1.plot(*tip_over_constraint.xy)

ax1.scatter(*cg_position.coords.xy)

ax1.fill(*main_gear_wheel.exterior.xy, color="black")
ax1.fill(*nose_gear_wheel.exterior.xy, color="black")
ax1.fill(*compressed_main_wheel.exterior.xy, color="blue")
ax1.plot(*floor_line.xy, color="black")

ax2.set_aspect(1)
ax2.plot(*front_fuselage.exterior.xy, color="black")
ax2.plot(*wing_line.xy, color="black")
ax2.plot(*left_engine.exterior.xy, color="black")
ax2.plot(*right_engine.exterior.xy, color="black")

ax2.fill(*left_wheels.exterior.xy, color="orange")

plt.show()
