"""Ellipse Shape Class"""

import pygame
from .base import Shape
from config import PIXELS_PER_UNIT, POINT_RADIUS, WHITE


class Ellipse(Shape):
    """Ellipse Class"""
    def __init__(self, center_x, center_y, rx, ry, color, original_coords=None, zoom_level=1.0):
        super().__init__(color)
        # Store original mathematical coordinates
        self.original_center_x = center_x
        self.original_center_y = center_y
        self.rx = rx  # Horizontal radius
        self.ry = ry  # Vertical radius
        self.original_coords = original_coords
        self.zoom_level = zoom_level
    
    def draw(self, surface, center_x, center_y, zoom_level=1.0):
        if self.rx > 0 and self.ry > 0:
            # Recalculate screen position based on current zoom
            screen_x = center_x + int(self.original_center_x * PIXELS_PER_UNIT * zoom_level)
            screen_y = center_y - int(self.original_center_y * PIXELS_PER_UNIT * zoom_level)
            
            # Convert radii from coordinate units to pixels
            scaled_rx = int(self.rx * PIXELS_PER_UNIT * zoom_level)
            scaled_ry = int(self.ry * PIXELS_PER_UNIT * zoom_level)
            rect = pygame.Rect(
                screen_x - scaled_rx,
                screen_y - scaled_ry,
                scaled_rx * 2,
                scaled_ry * 2
            )
            pygame.draw.ellipse(surface, self.color, rect, 2)
            
            # Draw center point
            pygame.draw.circle(surface, self.color, (screen_x, screen_y), POINT_RADIUS, 0)
            
            # Draw coordinates label with modern styling
            if self.original_coords:
                label_font = pygame.font.Font(None, 18)
                coord_text = f"C({self.original_coords[0]},{self.original_coords[1]})"
                text_surface = label_font.render(coord_text, True, WHITE)
                text_x = screen_x - text_surface.get_width() // 2
                text_y = screen_y - scaled_ry - 25
                
                bg_rect = text_surface.get_rect(topleft=(text_x - 4, text_y - 2))
                bg_rect.inflate_ip(8, 6)
                pygame.draw.rect(surface, self.color, bg_rect, border_radius=5)
                pygame.draw.rect(surface, WHITE, bg_rect, 2, border_radius=5)
                surface.blit(text_surface, (text_x, text_y))
