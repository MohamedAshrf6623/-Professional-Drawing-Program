"""Grid and Axes Drawing"""

import pygame
from config import *


def draw_grid(screen, canvas_width, center_x, center_y, height, zoom_level):
    """Draw Professional Grid and Axes"""
    tiny_font = pygame.font.Font(None, FONT_TINY)
    quad_font = pygame.font.Font(None, FONT_SMALL)
    
    # Calculate grid spacing based on zoom
    grid_spacing = int(50 * zoom_level)
    
    # Draw subtle grid lines (only on canvas area)
    for x in range(0, canvas_width, grid_spacing):
        if x == center_x:
            continue  # Skip axis line
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height), 1)
    for y in range(0, height, grid_spacing):
        if y == center_y:
            continue  # Skip axis line
        pygame.draw.line(screen, GRID_COLOR, (0, y), (canvas_width, y), 1)
    
    # Draw main axes with professional styling
    pygame.draw.line(screen, AXIS_COLOR, (center_x, 0), (center_x, height), 3)
    pygame.draw.line(screen, AXIS_COLOR, (0, center_y), (canvas_width, center_y), 3)
    
    # Draw axis arrows
    arrow_size = 10
    # Y-axis arrow (up)
    pygame.draw.polygon(screen, AXIS_COLOR, [
        (center_x, 5),
        (center_x - arrow_size//2, 5 + arrow_size),
        (center_x + arrow_size//2, 5 + arrow_size)
    ])
    # X-axis arrow (right)
    pygame.draw.polygon(screen, AXIS_COLOR, [
        (canvas_width - 5, center_y),
        (canvas_width - 5 - arrow_size, center_y - arrow_size//2),
        (canvas_width - 5 - arrow_size, center_y + arrow_size//2)
    ])
    
    # Y-axis arrow (down)
    pygame.draw.polygon(screen, AXIS_COLOR, [
        (center_x, height - 5),                         # tip (down)
        (center_x - arrow_size // 2, height - 5 - arrow_size),
        (center_x + arrow_size // 2, height - 5 - arrow_size)
    ])
    # X-axis arrow (right)
    pygame.draw.polygon(screen, AXIS_COLOR, [
        (5, center_y),                                  # tip (left)
        (5 + arrow_size, center_y - arrow_size // 2),
        (5 + arrow_size, center_y + arrow_size // 2)
    ])

    # Draw axis numbers with professional styling
    # X-axis numbers (horizontal) - Every 1 unit (but show every 5 units for clarity)
    for i in range(X_MIN, X_MAX + 1):
        x_pos = center_x + int(i * PIXELS_PER_UNIT * zoom_level)
        # Prevents drawing ticks Too close to edges
        if 20 < x_pos < canvas_width - 20:
            if i % 10 == 0 and i != 0:
                # Major tick marks every 10 units
                pygame.draw.line(screen, AXIS_COLOR, (x_pos, center_y - 6), (x_pos, center_y + 6), 2)
                num_text = tiny_font.render(str(i), True, DARK_GRAY)
                text_rect = num_text.get_rect(center=(x_pos, center_y + 18))
                pygame.draw.rect(screen, CANVAS_BG, text_rect.inflate(4, 2))
                screen.blit(num_text, text_rect)
            elif i % 5 == 0:
                # Medium tick marks every 5 units
                pygame.draw.line(screen, AXIS_COLOR, (x_pos, center_y - 4), (x_pos, center_y + 4), 1)
            else:
                # Minor tick marks every 1 unit
                pygame.draw.line(screen, GRID_COLOR, (x_pos, center_y - 2), (x_pos, center_y + 2), 1)
    
    # Y-axis numbers (vertical) - Every 1 unit (but show every 5 units for clarity)
    for i in range(Y_MIN, Y_MAX + 1):
        y_pos = center_y - int(i * PIXELS_PER_UNIT * zoom_level)
        if 20 < y_pos < height - 20:
            if i % 10 == 0 and i != 0:
                # Major tick marks every 10 units
                pygame.draw.line(screen, AXIS_COLOR, (center_x - 6, y_pos), (center_x + 6, y_pos), 2)
                num_text = tiny_font.render(str(i), True, DARK_GRAY)
                text_rect = num_text.get_rect(center=(center_x + 20, y_pos))
                pygame.draw.rect(screen, CANVAS_BG, text_rect.inflate(4, 2))
                screen.blit(num_text, text_rect)
            elif i % 5 == 0:
                # Medium tick marks every 5 units
                pygame.draw.line(screen, AXIS_COLOR, (center_x - 4, y_pos), (center_x + 4, y_pos), 1)
            else:
                # Minor tick marks every 1 unit
                pygame.draw.line(screen, GRID_COLOR, (center_x - 2, y_pos), (center_x + 2, y_pos), 1)
    
    # Draw origin label with background
    origin_text = tiny_font.render("0", True, AXIS_COLOR)
    origin_rect = origin_text.get_rect(center=(center_x - 15, center_y + 15))
    pygame.draw.rect(screen, CANVAS_BG, origin_rect.inflate(4, 2))
    screen.blit(origin_text, origin_rect)
    
    # Draw zoom level indicator with modern styling
    from .renderer import draw_gradient_rect
    
    small_font = pygame.font.Font(None, FONT_SMALL)
    zoom_rect = pygame.Rect(canvas_width - 120, 10, 110, 30)
    draw_gradient_rect(screen, zoom_rect, PANEL_HEADER, SECTION_BG, vertical=False)
    pygame.draw.rect(screen, ACCENT_BLUE, zoom_rect, 2, border_radius=6)
    zoom_text = small_font.render(f" {zoom_level:.1f}x", True, WHITE)
    screen.blit(zoom_text, (canvas_width - 110, 18))
    
    # Draw quadrant labels
    q1_text = quad_font.render("Q1 (+,+)", True, DARK_GRAY)
    q2_text = quad_font.render("Q2 (-,+)", True, DARK_GRAY)
    q3_text = quad_font.render("Q3 (-,-)", True, DARK_GRAY)
    q4_text = quad_font.render("Q4 (+,-)", True, DARK_GRAY)
    
    screen.blit(q1_text, (center_x + 10, 10))
    screen.blit(q2_text, (10, 10))
    screen.blit(q3_text, (10, height - 30))
    screen.blit(q4_text, (center_x + 10, height - 30))
