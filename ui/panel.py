"""Input Panel Drawing and Interaction"""

import pygame
from config import *
from drawing.renderer import draw_gradient_rect, draw_button_3d
from utils.coordinates import coordinate_to_screen


# Global state for input panel
panel_scroll_offset = 0
panel_content_height = 0
max_scroll = 0


def init_input_fields(current_tool):
    """Initialize input fields based on current tool"""
    if current_tool == "circle":
        return {
            'cx': '',  # Center X
            'cy': '',  # Center Y
            'r': ''    # Radius
        }, 'cx'
    elif current_tool == "ellipse":
        return {
            'cx': '',  # Center X
            'cy': '',  # Center Y
            'rx': '',  # Horizontal Radius
            'ry': ''   # Vertical Radius
        }, 'cx'
    elif current_tool == "line":
        return {
            'x1': '',  # Start X
            'y1': '',  # Start Y
            'x2': '',  # End X
            'y2': ''   # End Y
        }, 'x1'


def draw_input_panel(screen, canvas_width, height, current_tool, current_color, 
                     input_fields, active_field, zoom_level, shapes, panel_scroll_offset):
    """Draw Professional Input Panel on the right side with scroll support"""
    global max_scroll, panel_content_height
    
    panel_x = canvas_width
    
    # Panel background with gradient
    panel_rect = pygame.Rect(panel_x, 0, INPUT_PANEL_WIDTH, height)
    draw_gradient_rect(screen, panel_rect, PANEL_BG, VERY_DARK_GRAY, vertical=True)
    
    # Left border accent
    pygame.draw.rect(screen, ACCENT_BLUE, (panel_x, 0, 4, height))
    
    # Header section (fixed, doesn't scroll)
    header_rect = pygame.Rect(panel_x, 0, INPUT_PANEL_WIDTH, 70)
    draw_gradient_rect(screen, header_rect, PANEL_HEADER, PANEL_BG, vertical=True)
    pygame.draw.line(screen, ACCENT_BLUE, (panel_x, 70), (panel_x + INPUT_PANEL_WIDTH, 70), 2)
    
    # Title with icon (fixed header)
    title_font = pygame.font.Font(None, FONT_LARGE)
    title_text = title_font.render("⚙ CONTROL PANEL", True, WHITE)
    title_shadow = title_font.render("⚙ CONTROL PANEL", True, BLACK)
    screen.blit(title_shadow, (panel_x + 22, 22))
    screen.blit(title_text, (panel_x + 20, 20))
    
    # Start drawing scrollable content (apply scroll offset)
    y_pos = 90 - panel_scroll_offset
    
    subtitle_font = pygame.font.Font(None, FONT_MEDIUM)
    font = pygame.font.Font(None, FONT_NORMAL)
    small_font = pygame.font.Font(None, FONT_SMALL)
    
    # Tool Selection Section
    section_rect = pygame.Rect(panel_x + 10, y_pos, INPUT_PANEL_WIDTH - 20, 160)
    pygame.draw.rect(screen, SECTION_BG, section_rect, border_radius=10)
    pygame.draw.rect(screen, ACCENT_BLUE, section_rect, 2, border_radius=10)
    
    tool_title = subtitle_font.render("🔧 SELECT TOOL", True, WHITE)
    screen.blit(tool_title, (panel_x + 25, y_pos + 10))
    y_pos += 45
    
    # Tool buttons with icons
    tools = [("⭕ Circle", "circle"), ("⬭ Ellipse", "ellipse"), ("📏 Line", "line")]
    for tool_name, tool_key in tools:
        btn_rect = pygame.Rect(panel_x + 25, y_pos, 250, 32)
        if current_tool == tool_key:
            draw_button_3d(screen, btn_rect, BTN_PRIMARY, tool_name, font, False)
        else:
            draw_button_3d(screen, btn_rect, BTN_SECONDARY, tool_name, font, False)
        y_pos += 40
    
    y_pos += 15
    
    # Color Selection Section
    section_rect = pygame.Rect(panel_x + 10, y_pos, INPUT_PANEL_WIDTH - 20, 190)
    pygame.draw.rect(screen, SECTION_BG, section_rect, border_radius=10)
    pygame.draw.rect(screen, ACCENT_GREEN, section_rect, 2, border_radius=10)
    
    color_title = subtitle_font.render("🎨 SELECT COLOR", True, WHITE)
    screen.blit(color_title, (panel_x + 25, y_pos + 10))
    y_pos += 45
    
    colors = [("Red", RED), ("Green", GREEN), ("Blue", BLUE), ("Cyan", CYAN),
              ("Magenta", MAGENTA), ("Yellow", YELLOW), ("Orange", ORANGE), ("Purple", PURPLE)]
    
    for i in range(0, len(colors), 2):
        for j in range(2):
            if i + j < len(colors):
                color_name, color_val = colors[i + j]
                x_offset = panel_x + 25 + j * 125
                btn_rect = pygame.Rect(x_offset, y_pos, 115, 28)
                
                # 3D effect
                if current_color == color_val:
                    pygame.draw.rect(screen, HIGHLIGHT, btn_rect.inflate(8, 8), border_radius=6)
                    pygame.draw.rect(screen, color_val, btn_rect.inflate(4, 4), border_radius=5)
                else:
                    shadow_rect = btn_rect.copy()
                    shadow_rect.y += 2
                    pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=5)
                
                pygame.draw.rect(screen, color_val, btn_rect, border_radius=5)
                pygame.draw.rect(screen, WHITE if current_color == color_val else BLACK, btn_rect, 2, border_radius=5)
        y_pos += 33
    
    y_pos += 15
    
    # Input Fields Section
    num_fields = len(input_fields)
    section_height = 80 + num_fields * 38
    section_rect = pygame.Rect(panel_x + 10, y_pos, INPUT_PANEL_WIDTH - 20, section_height)
    pygame.draw.rect(screen, SECTION_BG, section_rect, border_radius=10)
    pygame.draw.rect(screen, CYAN, section_rect, 2, border_radius=10)
    
    input_title = subtitle_font.render("📝 ENTER VALUES", True, WHITE)
    screen.blit(input_title, (panel_x + 25, y_pos + 10))
    y_pos += 45
    
    # Determine fields based on current tool
    if current_tool == "circle":
        fields = [("Center X:", "cx"), ("Center Y:", "cy"), ("Radius:", "r")]
    elif current_tool == "ellipse":
        fields = [("Center X:", "cx"), ("Center Y:", "cy"), 
                  ("Radius X:", "rx"), ("Radius Y:", "ry")]
    else:  # line
        fields = [("Start X:", "x1"), ("Start Y:", "y1"), 
                  ("End X:", "x2"), ("End Y:", "y2")]
    
    for label, key in fields:
        # Label
        label_text = small_font.render(label, True, WHITE)
        screen.blit(label_text, (panel_x + 25, y_pos + 5))
        
        # Input field with modern styling
        field_x = panel_x + 115
        field_rect = pygame.Rect(field_x, y_pos, 160, 28)
        
        if active_field == key:
            # Active field - glowing effect
            glow_rect = field_rect.inflate(6, 6)
            pygame.draw.rect(screen, ACCENT_BLUE, glow_rect, border_radius=6)
            pygame.draw.rect(screen, WHITE, field_rect, border_radius=5)
        else:
            # Inactive field
            pygame.draw.rect(screen, LIGHT_GRAY, field_rect, border_radius=5)
        
        pygame.draw.rect(screen, DARK_GRAY, field_rect, 2, border_radius=5)
        
        # Input value
        value = input_fields.get(key, '')
        if value:
            value_text = font.render(value, True, BLACK)
            screen.blit(value_text, (field_x + 8, y_pos + 5))
        elif active_field == key:
            # Show cursor
            cursor_text = font.render("|", True, BLACK)
            screen.blit(cursor_text, (field_x + 8, y_pos + 3))
        
        y_pos += 38
    
    y_pos += 20
    
    # Action buttons section
    # Draw button
    draw_btn_rect = pygame.Rect(panel_x + 30, y_pos, 240, 45)
    draw_button_3d(screen, draw_btn_rect, BTN_SUCCESS, "✓ DRAW SHAPE", title_font, False)
    y_pos += 55
    
    # Clear button
    clear_btn_rect = pygame.Rect(panel_x + 30, y_pos, 240, 40)
    draw_button_3d(screen, clear_btn_rect, BTN_DANGER, "🗑 Clear All", font, False)
    y_pos += 50
    
    # Zoom controls section
    section_rect = pygame.Rect(panel_x + 10, y_pos, INPUT_PANEL_WIDTH - 20, 140)
    pygame.draw.rect(screen, SECTION_BG, section_rect, border_radius=10)
    pygame.draw.rect(screen, ORANGE, section_rect, 2, border_radius=10)
    
    zoom_title = subtitle_font.render("🔍 ZOOM CONTROLS", True, WHITE)
    screen.blit(zoom_title, (panel_x + 25, y_pos + 10))
    y_pos += 45
    
    # Zoom buttons in a row
    zoom_in_rect = pygame.Rect(panel_x + 30, y_pos, 110, 35)
    draw_button_3d(screen, zoom_in_rect, BTN_INFO, "➕ Zoom", font, False)
    
    zoom_out_rect = pygame.Rect(panel_x + 160, y_pos, 110, 35)
    draw_button_3d(screen, zoom_out_rect, BTN_WARNING, "➖ Zoom", font, False)
    y_pos += 45
    
    # Reset Zoom button
    reset_zoom_rect = pygame.Rect(panel_x + 30, y_pos, 240, 32)
    draw_button_3d(screen, reset_zoom_rect, BTN_SECONDARY, "↺ Reset (F5)", font, False)
    y_pos += 45
    
    # Calculate total content height and max scroll
    panel_content_height = y_pos + panel_scroll_offset + 40  # Add padding at bottom
    max_scroll = max(0, panel_content_height - height)
    
    # Draw scrollbar if content is larger than panel
    if panel_content_height > height:
        # Scrollbar background
        scrollbar_x = panel_x + INPUT_PANEL_WIDTH - 15
        scrollbar_bg_rect = pygame.Rect(scrollbar_x, 70, 10, height - 70)
        pygame.draw.rect(screen, VERY_DARK_GRAY, scrollbar_bg_rect, border_radius=5)
        
        # Scrollbar handle
        scroll_ratio = panel_scroll_offset / max_scroll if max_scroll > 0 else 0
        visible_ratio = height / panel_content_height
        handle_height = max(30, int((height - 70) * visible_ratio))
        handle_y = 70 + int((height - 70 - handle_height) * scroll_ratio)
        
        handle_rect = pygame.Rect(scrollbar_x, handle_y, 10, handle_height)
        pygame.draw.rect(screen, ACCENT_BLUE, handle_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, handle_rect, 1, border_radius=5)


def handle_panel_click(pos, canvas_width, height, current_tool, input_fields, 
                      panel_scroll_offset, shapes, center_x, center_y, zoom_level):
    """Handle clicks on the input panel with scroll support"""
    x, y_raw = pos
    panel_x = canvas_width
    
    # Check if click is in panel area
    if x < panel_x:
        return None, None, None
    
    # Adjust y coordinate for scroll offset (only for content below header)
    if y_raw < 70:
        # Header area - no scroll adjustment
        return None, None, None
    else:
        # Content area - adjust for scroll
        y = y_raw + panel_scroll_offset
    
    # Tool selection buttons (adjusted for scroll)
    base_y = 90
    if base_y + 30 <= y <= base_y + 65 and panel_x + 25 <= x <= panel_x + 275:
        return "circle", None, None
    elif base_y + 75 <= y <= base_y + 110 and panel_x + 25 <= x <= panel_x + 275:
        return "ellipse", None, None
    elif base_y + 120 <= y <= base_y + 155 and panel_x + 25 <= x <= panel_x + 275:
        return "line", None, None
    
    # Color selection buttons (adjusted for scroll)
    color_base = base_y + 175 + 45  # 310
    
    if color_base <= y <= color_base + 33:
        if panel_x + 25 <= x <= panel_x + 140:
            return None, RED, None
        elif panel_x + 150 <= x <= panel_x + 265:
            return None, GREEN, None
    elif color_base + 33 <= y <= color_base + 66:
        if panel_x + 25 <= x <= panel_x + 140:
            return None, BLUE, None
        elif panel_x + 150 <= x <= panel_x + 265:
            return None, CYAN, None
    elif color_base + 66 <= y <= color_base + 99:
        if panel_x + 25 <= x <= panel_x + 140:
            return None, MAGENTA, None
        elif panel_x + 150 <= x <= panel_x + 265:
            return None, YELLOW, None
    elif color_base + 99 <= y <= color_base + 132:
        if panel_x + 25 <= x <= panel_x + 140:
            return None, ORANGE, None
        elif panel_x + 150 <= x <= panel_x + 265:
            return None, PURPLE, None
    
    # Input fields - check exact position for each field
    field_y_start = 502
    field_height = 38
    fields = list(input_fields.keys())
    
    for i, key in enumerate(fields):
        field_y = field_y_start + i * field_height
        field_x = panel_x + 115
        if field_y <= y < field_y + 28 and field_x <= x <= field_x + 160:
            return None, None, key
    
    # Action buttons
    draw_btn_y = field_y_start + len(fields) * field_height + 20
    if draw_btn_y <= y <= draw_btn_y + 45 and panel_x + 30 <= x <= panel_x + 270:
        return "draw_shape", None, None
    
    clear_btn_y = draw_btn_y + 55
    if clear_btn_y <= y <= clear_btn_y + 40 and panel_x + 30 <= x <= panel_x + 270:
        return "clear_all", None, None
    
    # Zoom buttons
    zoom_section_y = clear_btn_y + 50
    zoom_btn_y = zoom_section_y + 45
    
    if zoom_btn_y <= y <= zoom_btn_y + 35:
        if panel_x + 30 <= x <= panel_x + 140:
            return "zoom_in", None, None
        elif panel_x + 160 <= x <= panel_x + 270:
            return "zoom_out", None, None
    
    reset_zoom_y = zoom_btn_y + 45
    if reset_zoom_y <= y <= reset_zoom_y + 32 and panel_x + 30 <= x <= panel_x + 270:
        return "reset_zoom", None, None
    
    return None, None, None
