"""Shape creation factory"""

from shapes import Circle, Ellipse, Line


def create_shape_from_input(current_tool, input_fields, current_color, center_x, center_y, zoom_level):
    """Create shape from input field values"""
    try:
        if current_tool == "circle":
            cx_str = input_fields.get('cx', '0').strip()
            cy_str = input_fields.get('cy', '0').strip()
            r_str = input_fields.get('r', '0').strip()
            
            cx = int(cx_str) if cx_str else 0
            cy = int(cy_str) if cy_str else 0
            r = int(r_str) if r_str else 0
            
            if r > 0:
                return Circle(cx, cy, r, current_color, (cx, cy), zoom_level)
        
        elif current_tool == "ellipse":
            cx_str = input_fields.get('cx', '0').strip()
            cy_str = input_fields.get('cy', '0').strip()
            rx_str = input_fields.get('rx', '0').strip()
            ry_str = input_fields.get('ry', '0').strip()
            
            cx = int(cx_str) if cx_str else 0
            cy = int(cy_str) if cy_str else 0
            rx = int(rx_str) if rx_str else 0
            ry = int(ry_str) if ry_str else 0
            
            if rx > 0 and ry > 0:
                return Ellipse(cx, cy, rx, ry, current_color, (cx, cy), zoom_level)
        
        elif current_tool == "line":
            x1_str = input_fields.get('x1', '0').strip()
            y1_str = input_fields.get('y1', '0').strip()
            x2_str = input_fields.get('x2', '0').strip()
            y2_str = input_fields.get('y2', '0').strip()
            
            x1 = int(x1_str) if x1_str else 0
            y1 = int(y1_str) if y1_str else 0
            x2 = int(x2_str) if x2_str else 0
            y2 = int(y2_str) if y2_str else 0
            
            return Line(x1, y1, x2, y2, current_color, (x1, y1, x2, y2), zoom_level)
    
    except (ValueError, KeyError):
        pass
    
    return None
