"""Diameter Fuselage"""

import math
import matplotlib.pyplot as plt
import shapely

from smallest_enclosing_circle import make_circle

# DESIGN PARAMETERS:

n_passengers = 72  # [-]
n_aisle = 1

# ADSEE I Reader - Table 5.3:
seat_width = 0.43  # [m]
seat_pitch = 0.76  # [m]
armrest_width = 0.05  # [m]

# ADSEE I Reader - Table 5.4:
h_armrest = 0.64  # [m]
w_aisle = 0.51  # [m]

h_shoulder = 1  # [m]
h_headroom = 1.35  # [m]
w_clearance = 0.02  # [m]
h_aisle = 1.80  # [m]
k_cabin = 1.08  # [m] from ADSEE reader
# [-] tail cone length ratio (tail length ratio irrelevant since we look for overall length)
tc_ratio = 2.5
# [-] nose cone length ratio (nose length ratio irrelevant since we look for overall length)
nc_ratio = 1.8


def calculate_cabin_width(w_clearance, w_aisle, w_seat, w_armrest, seats_abreast, n_aisle):
    return seats_abreast * w_seat + (seats_abreast + n_aisle + 1) * w_armrest + n_aisle * w_aisle + 2 * w_clearance


def calculate_floor_width(w_cabin, w_armrest, w_clearance):
    return w_cabin - 2*(w_armrest + w_clearance)


def calculate_headroom_width(w_floor, w_seat):
    return w_floor - w_seat

# ---

# DERIVED PARAMETERS:


# TODO: Maybe change round up/down
seats_abreast = math.ceil(0.45 * math.sqrt(n_passengers))  # [-]
n_rows = n_passengers / seats_abreast

print(f"Seats Abreast: {seats_abreast}")
print(f"Number of Rows: {n_rows:.0f}")

w_cabin = calculate_cabin_width(
    w_clearance, w_aisle, seat_width, armrest_width, seats_abreast, n_aisle)  # [m]
w_floor = calculate_floor_width(w_cabin, armrest_width, w_clearance)  # [m]
w_headroom = calculate_headroom_width(w_floor, seat_width)  # [m]

# Aisle position
# x_left_aisle = (w_floor / 2) - (w_aisle / 2)
# x_left_aisle = armrest_width + seat_width

x_left_aisle = math.floor(seats_abreast / (n_aisle + 1)
                          ) * (seat_width + armrest_width)

points = []

# "Legs" Box
armrest_box = shapely.box(0, 0, w_floor, h_armrest)
shoulder_box = shapely.box(
    (w_floor / 2) - (w_cabin / 2), h_armrest, (w_floor / 2) + (w_cabin / 2), h_shoulder)
head_box = shapely.box((w_floor / 2) - (w_headroom / 2),
                       h_shoulder, (w_floor / 2) + (w_headroom / 2), h_headroom)
aisle_box = shapely.box(x_left_aisle, 0, x_left_aisle + w_aisle, h_aisle)

points.extend(armrest_box.exterior.coords)
points.extend(shoulder_box.exterior.coords)
points.extend(head_box.exterior.coords)
points.extend(aisle_box.exterior.coords)

# Fuselage Smallest Circle
fus_center_x, fus_center_y, fus_radius = make_circle(points)

d_fus_inner = 2 * fus_radius

# Eq. 5.3 (ADSEE I):
d_fus_outer = 1.045 * d_fus_inner + 0.084  # [m]
print(f"Fuselage Inner Diameter: {d_fus_inner} [m]")
print(f"Fuselage Outer Diameter: {d_fus_outer} [m]")

# Cabin length

l_cabin = k_cabin*n_passengers/seats_abreast

l_fus = (tc_ratio + nc_ratio)*d_fus_outer + l_cabin

print(f"Fuslege length: {l_fus} [m]")

# Draw fuselage
fig, ax = plt.subplots()
ax.set_aspect(1)

ax.fill(*armrest_box.exterior.xy, edgecolor="lightpink",
        facecolor="lightpink", alpha=0.5, linewidth=2)
ax.fill(*head_box.exterior.xy, edgecolor="lightskyblue",
        facecolor="lightskyblue", alpha=0.5, linewidth=2)
ax.fill(*shoulder_box.exterior.xy, edgecolor="springgreen",
        facecolor="springgreen", alpha=0.5, linewidth=2)
ax.fill(*aisle_box.exterior.xy, edgecolor="darkorchid",
        facecolor="darkorchid", alpha=0.5, linewidth=2)

# Cargo Volume Calculation
fuselage_circle = shapely.Point(fus_center_x, fus_center_y).buffer(fus_radius)
ax.plot(*fuselage_circle.exterior.xy, linewidth=3)

# Floor Line
floor_box = shapely.box(0, -1, w_floor, 0)
cabin_box = shapely.box(-1, 0, 5, 5)

# Cargo Polygon
cargo_polygon = fuselage_circle.intersection(floor_box)
ax.fill(*cargo_polygon.exterior.xy, facecolor="lightsalmon",
        edgecolor="orangered", linewidth=3)

cargo_area = cargo_polygon.area
cargo_volume = cargo_area * l_cabin

# Cabin Volume
cabin_polygon = fuselage_circle.intersection(cabin_box)
ax.fill(*cabin_polygon.exterior.xy)

cabin_area = cabin_polygon.area
cabin_volume = cabin_area * l_cabin

print(f"Cargo Volume: {cargo_volume} [m^3]")
print(f"Cabin Volume: {cabin_volume} [m^3]")


plt.show()
