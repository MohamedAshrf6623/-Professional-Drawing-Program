"""Coordinate conversion utilities"""

from config import PIXELS_PER_UNIT


def coordinate_to_screen(x, y, center_x, center_y, zoom_level):
    """Convert mathematical coordinates to screen coordinates with zoom"""
    screen_x = center_x + int(x * PIXELS_PER_UNIT * zoom_level)
    screen_y = center_y - int(y * PIXELS_PER_UNIT * zoom_level)
    return (screen_x, screen_y)


def screen_to_coordinate(screen_x, screen_y, center_x, center_y, zoom_level):
    """Convert screen coordinates to mathematical coordinates with zoom"""
    x = int((screen_x - center_x) / (PIXELS_PER_UNIT * zoom_level))
    y = int((center_y - screen_y) / (PIXELS_PER_UNIT * zoom_level))
    return (x, y)
