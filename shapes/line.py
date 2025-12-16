"""Line Shape Class"""

import pygame
from .base import Shape
from config import LINE_WIDTH, POINT_SIZE, WHITE, PIXELS_PER_UNIT


class Line(Shape):
    """Line Class"""
    def __init__(self, x1, y1, x2, y2, color, original_coords=None, zoom_level=1.0):
        super().__init__(color)
        # Store original mathematical coordinates
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.original_coords = original_coords  # (x1, y1, x2, y2)
        self.zoom_level = zoom_level
    
    def draw(self, surface, center_x, center_y, zoom_level=1.0):
        # Recalculate screen positions based on current zoom
        start_x = center_x + int(self.x1 * PIXELS_PER_UNIT * zoom_level)
        start_y = center_y - int(self.y1 * PIXELS_PER_UNIT * zoom_level)
        end_x = center_x + int(self.x2 * PIXELS_PER_UNIT * zoom_level)
        end_y = center_y - int(self.y2 * PIXELS_PER_UNIT * zoom_level)
        
        pygame.draw.line(surface, self.color, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
        
        # Draw start and end points
        pygame.draw.circle(surface, self.color, (start_x, start_y), POINT_SIZE, 0)
        pygame.draw.circle(surface, self.color, (end_x, end_y), POINT_SIZE, 0)
        
        # Draw coordinates labels with modern styling
        if self.original_coords:
            label_font = pygame.font.Font(None, 16)
            
            # Start point label
            start_text = f"({self.original_coords[0]},{self.original_coords[1]})"
            start_surface = label_font.render(start_text, True, WHITE)
            label_start_x = start_x + 8
            label_start_y = start_y - 22
            bg_rect = start_surface.get_rect(topleft=(label_start_x - 3, label_start_y - 2))
            bg_rect.inflate_ip(6, 4)
            pygame.draw.rect(surface, self.color, bg_rect, border_radius=4)
            pygame.draw.rect(surface, WHITE, bg_rect, 2, border_radius=4)
            surface.blit(start_surface, (label_start_x, label_start_y))
            
            # End point label
            end_text = f"({self.original_coords[2]},{self.original_coords[3]})"
            end_surface = label_font.render(end_text, True, WHITE)
            label_end_x = end_x + 8
            label_end_y = end_y - 22
            bg_rect = end_surface.get_rect(topleft=(label_end_x - 3, label_end_y - 2))
            bg_rect.inflate_ip(6, 4)
            pygame.draw.rect(surface, self.color, bg_rect, border_radius=4)
            pygame.draw.rect(surface, WHITE, bg_rect, 2, border_radius=4)
            surface.blit(end_surface, (label_end_x, label_end_y))
