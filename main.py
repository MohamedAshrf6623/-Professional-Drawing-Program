"""
Professional Drawing Program - Input Based
Main entry point
"""

import pygame
import sys
import os

from config import *
from drawing import draw_grid
from ui.panel import draw_input_panel, handle_panel_click, init_input_fields
from utils.shapes_factory import create_shape_from_input


# =====================
# Initialization
# =====================
pygame.init()

# Center window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Screen size (half of display)
info = pygame.display.Info()
WIDTH = info.current_w // 2
HEIGHT = info.current_h // 2

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Professional Drawing Program - Input Based")

clock = pygame.time.Clock()

# =====================
# Application State
# =====================
CANVAS_WIDTH = WIDTH - INPUT_PANEL_WIDTH
center_x = CANVAS_WIDTH // 2
center_y = HEIGHT // 2

current_tool = DEFAULT_TOOL
current_color = DEFAULT_COLOR

shapes = []

# Zoom settings
zoom_level = DEFAULT_ZOOM

# Scroll state for panel
panel_scroll_offset = 0

# Input fields state
input_fields, active_field = init_input_fields(current_tool)
active_field = None


# =====================
# Helpers Functions
# =====================
def update_window_size(w, h):
    """Update window dimensions"""
    global WIDTH, HEIGHT, CANVAS_WIDTH, center_x, center_y, screen
    WIDTH, HEIGHT = w, h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    CANVAS_WIDTH = WIDTH - INPUT_PANEL_WIDTH
    center_x = CANVAS_WIDTH // 2
    center_y = HEIGHT // 2


def handle_keyboard(event):
    """Handle keyboard shortcuts"""
    global zoom_level, active_field, input_fields, shapes

    if event.key == pygame.K_RETURN:
        # ENTER -> create shape using Factory
        shape = create_shape_from_input(
            current_tool, input_fields, current_color,
            center_x, center_y, zoom_level
        )
        if shape:
            shapes.append(shape)
            reset_inputs()

    elif event.key == pygame.K_TAB and active_field:
        # TAB -> move to next input field
        keys = list(input_fields.keys())
        active_field = keys[(keys.index(active_field) + 1) % len(keys)]

    elif event.key == pygame.K_BACKSPACE and active_field:
        # BACKSPACE -> delete last character in active input field    
        input_fields[active_field] = input_fields[active_field][:-1]

    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
        # + or = -> zoom in
        zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)

    elif event.key == pygame.K_MINUS and not active_field:
        # - -> zoom out ONLY if not typing
        zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)

    elif event.key == pygame.K_F5:
        # F5 -> reset zoom
        zoom_level = DEFAULT_ZOOM

    elif event.key == pygame.K_DELETE and pygame.key.get_mods() & pygame.KMOD_CTRL:
        # CTRL + DELETE -> clear all shapes
        shapes.clear()

    elif event.unicode.isdigit() or event.unicode == '.' or event.unicode == '-':
        # Input numbers, dot or minus into active field
        if active_field:
            input_fields[active_field] += event.unicode


def reset_inputs():
    """Reset input fields for the current tool"""
    global input_fields, active_field
    input_fields, active_field = init_input_fields(current_tool)


def main():
    """Main game loop"""
    global current_tool, current_color, zoom_level, active_field, input_fields
    global panel_scroll_offset, shapes, CANVAS_WIDTH
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                update_window_size(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                handle_keyboard(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Scroll or zoom
                if event.button == 4:  # wheel up
                    if mouse_pos[0] >= CANVAS_WIDTH:
                        panel_scroll_offset = max(0, panel_scroll_offset - 30)
                    else:
                        zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)

                elif event.button == 5:  # wheel down
                    if mouse_pos[0] >= CANVAS_WIDTH:
                        panel_scroll_offset += 30
                    else:
                        zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)

                elif event.button == 1:  # left click
                    tool, color, field = handle_panel_click(
                        mouse_pos, CANVAS_WIDTH, HEIGHT,
                        current_tool, input_fields,
                        panel_scroll_offset, shapes,
                        center_x, center_y, zoom_level
                    )

                    if tool in ("circle", "ellipse", "line"):
                        current_tool = tool
                        reset_inputs()

                    elif tool == "draw_shape":
                        shape = create_shape_from_input(
                            current_tool, input_fields,
                            current_color, center_x,
                            center_y, zoom_level
                        )
                        if shape:
                            shapes.append(shape)
                            reset_inputs()

                    elif tool == "clear_all":
                        shapes.clear()

                    elif tool == "zoom_in":
                        zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)

                    elif tool == "zoom_out":
                        zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)

                    elif tool == "reset_zoom":
                        zoom_level = DEFAULT_ZOOM

                    if field:
                        active_field = field

                    if color:
                        current_color = color

        # =====================
        # Rendering
        # =====================
        screen.fill(CANVAS_BG)

        draw_grid(screen, CANVAS_WIDTH, center_x, center_y, HEIGHT, zoom_level)

        for shape in shapes:
            shape.draw(screen, center_x, center_y, zoom_level)

        panel_scroll_offset = draw_input_panel(
            screen, CANVAS_WIDTH, HEIGHT,
            current_tool, current_color,
            input_fields, active_field,
            zoom_level, shapes,
            panel_scroll_offset
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
