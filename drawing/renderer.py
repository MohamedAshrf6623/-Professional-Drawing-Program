"""Rendering helper functions"""

import pygame
from config import *


def draw_rounded_rect(surface, color, rect, radius=10):
    """Draw a rounded rectangle"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_gradient_rect(surface, rect, color1, color2, vertical=True):
    """Draw a gradient rectangle"""
    if vertical:
        for i in range(rect.height):
            alpha = i / rect.height
            r = int(color1[0] * (1 - alpha) + color2[0] * alpha)
            g = int(color1[1] * (1 - alpha) + color2[1] * alpha)
            b = int(color1[2] * (1 - alpha) + color2[2] * alpha)
            pygame.draw.rect(surface, (r, g, b), 
                           (rect.x, rect.y + i, rect.width, 1))
    else:
        for i in range(rect.width):
            alpha = i / rect.width
            r = int(color1[0] * (1 - alpha) + color2[0] * alpha)
            g = int(color1[1] * (1 - alpha) + color2[1] * alpha)
            b = int(color1[2] * (1 - alpha) + color2[2] * alpha)
            pygame.draw.rect(surface, (r, g, b), 
                           (rect.x + i, rect.y, 1, rect.height))


def draw_button_3d(surface, rect, color, text, font_obj, pressed=False):
    """Draw a 3D button with shadow"""
    # Shadow
    if not pressed:
        shadow_rect = rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, VERY_DARK_GRAY, shadow_rect, border_radius=8)
    
    # Button
    button_rect = rect.copy()
    if pressed:
        button_rect.y += 2
    
    # Gradient effect (lighter top, darker bottom)
    for i in range(rect.height):
        alpha = i / rect.height
        r = int(color[0] * (1 - alpha * 0.2))
        g = int(color[1] * (1 - alpha * 0.2))
        b = int(color[2] * (1 - alpha * 0.2))
        pygame.draw.rect(surface, (r, g, b), 
                        (button_rect.x, button_rect.y + i, button_rect.width, 1))
    
    pygame.draw.rect(surface, BLACK, button_rect, 2, border_radius=8)
    
    # Text
    text_surface = font_obj.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
