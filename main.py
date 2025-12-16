"""
Professional Drawing Program - Input Based
Main entry point
"""

import pygame
import sys
import os

# Configuration
from config import *

# Shapes
from shapes import Circle, Ellipse, Line

# Drawing
from drawing import draw_grid
from drawing.renderer import draw_gradient_rect

# UI
from ui.panel import draw_input_panel, handle_panel_click, init_input_fields

# Utils
from utils.coordinates import coordinate_to_screen
from utils.shapes_factory import create_shape_from_input


# Initialize Pygame
pygame.init()

# Get screen info to position window in center
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

# Screen Settings - Set to half of screen size
WIDTH = screen_width // 2
HEIGHT = screen_height // 2

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Professional Drawing Program - Input Based")

# Center the window on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.quit()
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Drawing Settings
CANVAS_WIDTH = WIDTH - INPUT_PANEL_WIDTH
center_x = CANVAS_WIDTH // 2
center_y = HEIGHT // 2
current_tool = DEFAULT_TOOL
current_color = DEFAULT_COLOR
shapes = []

# Zoom settings
zoom_level = DEFAULT_ZOOM

# Window state
is_fullscreen = False

# Scroll state for panel
panel_scroll_offset = 0
panel_content_height = 0
max_scroll = 0

# Input fields state
input_fields, active_field = init_input_fields(current_tool)

# Fonts
font = pygame.font.Font(None, FONT_NORMAL)
title_font = pygame.font.Font(None, FONT_LARGE)
subtitle_font = pygame.font.Font(None, FONT_MEDIUM)
small_font = pygame.font.Font(None, FONT_SMALL)
tiny_font = pygame.font.Font(None, FONT_TINY)


def update_window_size(new_width, new_height):
    """Update window dimensions"""
    global WIDTH, HEIGHT, CANVAS_WIDTH, center_x, center_y, screen
    WIDTH = new_width
    HEIGHT = new_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    CANVAS_WIDTH = WIDTH - INPUT_PANEL_WIDTH
    center_x = CANVAS_WIDTH // 2
    center_y = HEIGHT // 2


def handle_input(event):
    """Handle keyboard input"""
    global active_field, input_fields, current_tool, zoom_level, is_fullscreen, shapes
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            # Submit and create shape
            shape = create_shape_from_input(current_tool, input_fields, current_color, 
                                           center_x, center_y, zoom_level)
            if shape:
                shapes.append(shape)
                input_fields, active_field = init_input_fields(current_tool)
        
        elif event.key == pygame.K_TAB:
            # Move to next field
            keys = list(input_fields.keys())
            if active_field in keys:
                current_index = keys.index(active_field)
                active_field = keys[(current_index + 1) % len(keys)]
        
        elif event.key == pygame.K_BACKSPACE:
            # Delete character
            if active_field and input_fields.get(active_field):
                input_fields[active_field] = input_fields[active_field][:-1]
        
        elif event.key == pygame.K_DELETE:
            # Delete all shapes
            shapes.clear()
        
        elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
            # Zoom in with keyboard
            zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)
        
        elif event.key == pygame.K_MINUS:
            # Zoom out with keyboard
            if not active_field:
                zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)
            else:
                # Allow minus in input fields
                input_fields[active_field] = input_fields.get(active_field, '') + '-'
        
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_F11:
            # Toggle fullscreen
            pygame.display.toggle_fullscreen()
            is_fullscreen = not is_fullscreen
        
        elif event.key == pygame.K_F5:
            # Reset zoom with F5
            zoom_level = DEFAULT_ZOOM
        
        elif event.unicode.isdigit() or event.unicode == '.':
            # Add digit or decimal point (0-9 and .)
            if active_field and active_field in input_fields:
                input_fields[active_field] = input_fields.get(active_field, '') + event.unicode


def main():
    """Main game loop"""
    global current_tool, current_color, zoom_level, active_field, input_fields
    global panel_scroll_offset, max_scroll, shapes, WIDTH, HEIGHT, CANVAS_WIDTH
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                update_window_size(event.w, event.h)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    tool, color, field = handle_panel_click(
                        mouse_pos, CANVAS_WIDTH, HEIGHT, current_tool, 
                        input_fields, panel_scroll_offset, shapes, 
                        center_x, center_y, zoom_level
                    )
                    
                    if tool == "circle":
                        current_tool = "circle"
                        input_fields, active_field = init_input_fields(current_tool)
                    elif tool == "ellipse":
                        current_tool = "ellipse"
                        input_fields, active_field = init_input_fields(current_tool)
                    elif tool == "line":
                        current_tool = "line"
                        input_fields, active_field = init_input_fields(current_tool)
                    elif tool == "draw_shape":
                        shape = create_shape_from_input(current_tool, input_fields, 
                                                       current_color, center_x, center_y, zoom_level)
                        if shape:
                            shapes.append(shape)
                            input_fields, active_field = init_input_fields(current_tool)
                    elif tool == "clear_all":
                        shapes.clear()
                    elif tool == "zoom_in":
                        zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)
                    elif tool == "zoom_out":
                        zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)
                    elif tool == "reset_zoom":
                        zoom_level = DEFAULT_ZOOM
                    elif field:
                        active_field = field
                    
                    if color:
                        current_color = color
                
                elif event.button == 4:  # Mouse wheel up
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= CANVAS_WIDTH:
                        # Scroll panel up
                        panel_scroll_offset = max(0, panel_scroll_offset - 30)
                    else:
                        # Zoom in on canvas
                        zoom_level = min(zoom_level + ZOOM_STEP, MAX_ZOOM)
                
                elif event.button == 5:  # Mouse wheel down
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] >= CANVAS_WIDTH:
                        # Scroll panel down
                        panel_scroll_offset = panel_scroll_offset + 30
                    else:
                        # Zoom out on canvas
                        zoom_level = max(zoom_level - ZOOM_STEP, MIN_ZOOM)
            
            elif event.type == pygame.KEYDOWN:
                handle_input(event)
        
        # Draw everything
        screen.fill(CANVAS_BG)
        
        # Draw canvas area
        canvas_rect = pygame.Rect(0, 0, CANVAS_WIDTH, HEIGHT)
        pygame.draw.rect(screen, CANVAS_BG, canvas_rect)
        
        # Draw grid
        draw_grid(screen, CANVAS_WIDTH, center_x, center_y, HEIGHT, zoom_level)
        
        # Draw all saved shapes
        for shape in shapes:
            shape.draw(screen, center_x, center_y, zoom_level)
        
        # Draw input panel and update scroll offset
        panel_scroll_offset = draw_input_panel(screen, CANVAS_WIDTH, HEIGHT, current_tool, current_color,
                        input_fields, active_field, zoom_level, shapes, panel_scroll_offset)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
