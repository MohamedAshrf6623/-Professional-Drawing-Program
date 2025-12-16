"""Base Shape Class"""


class Shape:
    """Base Shape Class"""
    def __init__(self, color):
        self.color = color
    
    def draw(self, surface):
        """Draw shape on surface - override in subclasses"""
        pass
