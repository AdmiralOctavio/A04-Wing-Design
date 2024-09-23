import math
import os

import numpy as np
import yaml
import pygame
import pygame.freetype

from utils import load_airfoil_data, polygon_area, lerp

WING_VOLUME_SAMPLE_COUNT = 10000


def calculate_quarter_chord_sweep_angle(cruise_mach: float) -> float:
    # From eq. 8.1 in ADSEE I reader
    if cruise_mach < 0.66:
        return 0
    else:
        return math.acos(1.16 / (cruise_mach + 0.5))


def calculate_taper_ratio(quarter_chord_sweep_angle: float) -> float:
    # Eq. 8.3 in ADSEE I reader
    return 0.2 * (2 - math.radians(quarter_chord_sweep_angle))


def calculate_wing_span(wing_area: float, aspect_ratio: float) -> float:
    # Eq. 8.4 in ADSEE I reader
    return math.sqrt(wing_area * aspect_ratio)


def calculate_root_chord(wing_area: float, taper_ratio: float, wing_span: float) -> float:
    # Eq. 8.5 in ADSEE I reader
    return (2 * wing_area) / ((1 + taper_ratio) * wing_span)


def calculate_tip_chord(taper_ratio: float, root_chord: float) -> float:
    # Eq. 8.6 in ADSEE I reader
    return taper_ratio * root_chord


def calculate_chord_along_span(root_chord: float, tip_chord: float, quarter_chord_sweep_angle: float,
                               half_span: float, span_pos: np.ndarray) -> np.ndarray:
    root_leading_edge_y = 0
    root_quarter_chord_y = 0.25 * root_chord
    root_trailing_edge_y = root_chord

    tip_quarter_chord_y = root_quarter_chord_y + half_span * math.sin(quarter_chord_sweep_angle)
    tip_leading_edge_y = tip_quarter_chord_y - 0.25 * tip_chord
    tip_trailing_edge_y = tip_quarter_chord_y + 0.75 * tip_chord

    chord_leading_edge_y = lerp(root_leading_edge_y, tip_leading_edge_y, span_pos / half_span)
    chord_trailing_edge_y = lerp(root_trailing_edge_y, tip_trailing_edge_y, span_pos / half_span)

    return abs(chord_leading_edge_y - chord_trailing_edge_y)


def calculate_wing_volume_with_airfoil(airfoil_file: str, wing_span: float, root_chord: float, tip_chord: float,
                                       quarter_chord_sweep_angle: float) -> float:
    airfoil_points_x, airfoil_points_y = load_airfoil_data(airfoil_file)
    np_airfoil_x, np_airfoil_y = np.array(airfoil_points_x), np.array(airfoil_points_y)
    airfoil_unit_area = polygon_area(np_airfoil_x, np_airfoil_y)

    wing_volume_sample_points = np.linspace(0, wing_span / 2, WING_VOLUME_SAMPLE_COUNT)
    wing_chord_samples = calculate_chord_along_span(root_chord, tip_chord, quarter_chord_sweep_angle,
                                                    wing_span / 2, wing_volume_sample_points)
    wing_airfoil_area_samples = np.pow(wing_chord_samples, 2) * airfoil_unit_area
    wing_volume_sample_step = (wing_span / 2) / (WING_VOLUME_SAMPLE_COUNT - 1)
    wing_volume_samples = wing_airfoil_area_samples * wing_volume_sample_step
    wing_volume = np.sum(wing_volume_samples[:-1]) * 2

    return wing_volume


def draw_airfoil(screen: pygame.Surface, airfoil_center: tuple[float, float], chord_length: float,
                 geometry: list[tuple[float, float]]):
    for point_i in range(len(geometry)):
        start_point_raw = geometry[point_i]
        end_point_raw = geometry[(point_i + 1) % len(geometry)]

        start_point = (airfoil_center[0] - (chord_length / 2) + (chord_length * start_point_raw[0]),
                       airfoil_center[1] - chord_length * start_point_raw[1])

        end_point = (airfoil_center[0] - (chord_length / 2) + (chord_length * end_point_raw[0]),
                     airfoil_center[1] - chord_length * end_point_raw[1])

        pygame.draw.line(screen, "black", start_point, end_point, 2)


def main():
    # Load Parameters
    with open("aircraft_parameters.yaml") as file:
        aircraft_parameters = yaml.safe_load(file)

    requirements = aircraft_parameters["requirements"]
    wing_parameters = aircraft_parameters["wing"]

    cruise_mach = requirements["cruise_mach"]

    wing_area = wing_parameters["wing_area"]
    aspect_ratio = aircraft_parameters["aspect_ratio"]

    quarter_chord_sweep_angle = calculate_quarter_chord_sweep_angle(cruise_mach)
    taper_ratio = calculate_taper_ratio(quarter_chord_sweep_angle)
    wing_span = calculate_wing_span(wing_area, aspect_ratio)
    root_chord = calculate_root_chord(wing_area, taper_ratio, wing_span)
    tip_chord = calculate_tip_chord(taper_ratio, root_chord)

    wing_area = (root_chord + tip_chord) * (wing_span / 2)

    # print(f"quarter chord sweep angle = {math.degrees(quarter_chord_sweep_angle)} [deg]")
    # print(f"taper ratio = {taper_ratio} [-]")
    print(f"wing half span = {wing_span / 2:.2f} [m]")
    print(f"root chord = {root_chord / 2:.2f} [m]")
    print(f"tip chord = {tip_chord / 2:.2f} [m]")

    print(f"full wing area = {wing_area:.2f} [m^2]")

    airfoil_geometries = []
    wing_volumes = []
    airfoil_names = []

    for file in os.listdir("airfoils"):
        filename = os.fsdecode(file)
        if filename.endswith(".dat"):
            file_path = os.path.join("airfoils", filename)

            wing_volume = calculate_wing_volume_with_airfoil(
                file_path, wing_span, root_chord, tip_chord, quarter_chord_sweep_angle
            )

            airfoil_geometry = load_airfoil_data(file_path)

            airfoil_geometries.append(airfoil_geometry)
            wing_volumes.append(wing_volume)
            airfoil_names.append(filename.split(".")[0])

    # Init Pygame Window
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    pygame.font.init()
    text_renderer = pygame.freetype.SysFont('JetBrains Mono', 16)

    # Scale: 22m = 1000px
    scale = 20  # [-]
    scroll_sensitivity = 0.5  # [-]

    camera = (-350, -50)
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                scale += (-1 if event.flipped else 1) * event.y * scroll_sensitivity
                # roboto_mono.size = scale
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    camera = (camera[0] + event.rel[0], camera[1] + event.rel[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    print(camera, scale)

        screen.fill("white")

        # Root Chord
        root_chord_leading_edge = (camera[0] + 640, camera[1] + 100)
        root_chord_trailing_edge = (root_chord_leading_edge[0], root_chord_leading_edge[1] + root_chord * scale)
        pygame.draw.line(screen, "black", root_chord_leading_edge, root_chord_trailing_edge, 2)

        root_label, _ = text_renderer.render(f"{root_chord:.2f} m", "black")
        screen.blit(root_label, (root_chord_leading_edge[0] + 10,
                                 (root_chord_leading_edge[1] + root_chord_trailing_edge[1]) / 2))

        # Sweep Line
        quarter_root_chord = (root_chord_leading_edge[0], root_chord_leading_edge[1] + 0.25 * root_chord * scale)
        half_span = wing_span * scale * 0.5
        right_quarter_tip_chord = (root_chord_leading_edge[0] + half_span,
                                   quarter_root_chord[1] + half_span * math.sin(quarter_chord_sweep_angle))
        left_quarter_tip_chord = (root_chord_leading_edge[0] - half_span,
                                  quarter_root_chord[1] + half_span * math.sin(quarter_chord_sweep_angle))

        pygame.draw.line(screen, "orange", quarter_root_chord, right_quarter_tip_chord, 2)
        pygame.draw.line(screen, "orange", quarter_root_chord, left_quarter_tip_chord, 2)

        # Tip Chord
        right_tip_chord_leading_edge = (right_quarter_tip_chord[0],
                                        right_quarter_tip_chord[1] - tip_chord * 0.25 * scale)
        right_tip_chord_trailing_edge = (right_quarter_tip_chord[0],
                                         right_quarter_tip_chord[1] + tip_chord * 0.75 * scale)

        left_tip_chord_leading_edge = (left_quarter_tip_chord[0], left_quarter_tip_chord[1] - tip_chord * 0.25 * scale)
        left_tip_chord_trailing_edge = (left_quarter_tip_chord[0], left_quarter_tip_chord[1] + tip_chord * 0.75 * scale)

        pygame.draw.line(screen, "black", right_tip_chord_leading_edge, right_tip_chord_trailing_edge, 2)
        pygame.draw.line(screen, "black", left_tip_chord_leading_edge, left_tip_chord_trailing_edge, 2)

        tip_label, _ = text_renderer.render(f"{tip_chord:.2f} m", "black")
        screen.blit(tip_label, (right_tip_chord_leading_edge[0] + 10,
                                (right_tip_chord_leading_edge[1] + right_tip_chord_trailing_edge[1]) / 2))

        # Leading Edges
        pygame.draw.line(screen, "black", root_chord_leading_edge, right_tip_chord_leading_edge, 2)
        pygame.draw.line(screen, "black", root_chord_leading_edge, left_tip_chord_leading_edge, 2)

        # Trailing Edges
        pygame.draw.line(screen, "black", root_chord_trailing_edge, right_tip_chord_trailing_edge, 2)
        pygame.draw.line(screen, "black", root_chord_trailing_edge, left_tip_chord_trailing_edge, 2)

        # Airfoil
        for i in range(len(airfoil_geometries)):
            airfoil_chord_length = wing_span * scale
            airfoil_center = (root_chord_leading_edge[0], root_chord_leading_edge[1] + (root_chord + 5 + 4 * i) * scale)

            pygame.draw.line(screen, "red", (airfoil_center[0] - (airfoil_chord_length / 2), airfoil_center[1]),
                             (airfoil_center[0] + (airfoil_chord_length / 2), airfoil_center[1]), 2)

            airfoil_points = list(zip(*airfoil_geometries[i]))

            draw_airfoil(screen, airfoil_center, airfoil_chord_length, airfoil_points)

            airfoil_name = airfoil_names[i]
            wing_volume = wing_volumes[i]

            text_surface, text_rect = text_renderer.render(f"{airfoil_name}; wing volume of {wing_volume:.2f} [m^3]",
                                                           "black")
            screen.blit(text_surface, (airfoil_center[0] + (airfoil_chord_length / 2) + 20, airfoil_center[1] - 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    # calculate_all_files()
    main()
