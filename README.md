# Professional Drawing Program

A sophisticated 2D drawing application with a control panel interface, built with Pygame. This program enables precise shape creation through coordinate input and provides an interactive canvas with dynamic zoom and grid display.

## Features

- 🎨 **Multiple Shape Types** - Draw circles, ellipses, and lines with pixel-perfect precision
- 🎯 **Coordinate Input Panel** - Enter exact coordinates through an intuitive control panel
- 🔍 **Dynamic Zoom** - Smoothly zoom in and out of your canvas with mouse wheel or keyboard
- 🌐 **Professional Grid System** - Cartesian coordinate grid with axis labels and origin marker
- 🎪 **Modern UI** - Clean, user-friendly interface with visual feedback
- 🎨 **Color Palette** - 8 vibrant colors to choose from
- ⌨️ **Keyboard Shortcuts** - Efficient workflow with comprehensive hotkeys
- 📐 **Cartesian Coordinate System** - Traditional X-Y axes with origin at screen center

## Project Structure

```
project/
├── main.py                  # Main entry point and application loop
├── config.py               # Configuration, colors, and constants
├── requirements.txt        # Python dependencies
├── shapes/                 # Shape classes module
│   ├── __init__.py
│   ├── base.py            # Abstract base Shape class
│   ├── circle.py          # Circle implementation
│   ├── ellipse.py         # Ellipse implementation
│   └── line.py            # Line implementation
├── ui/                    # User interface module
│   ├── __init__.py
│   ├── panel.py           # Control panel UI
│   └── colors.py          # Color picker interface
├── drawing/               # Rendering module
│   ├── __init__.py
│   ├── grid.py            # Grid and axes rendering
│   └── renderer.py        # Helper drawing functions
└── utils/                 # Utility functions module
    ├── __init__.py
    ├── coordinates.py     # Coordinate transformation utilities
    └── shapes_factory.py  # Shape factory pattern implementation
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git (for cloning the repository)

### Setup

#### Option 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/MohamedAshrf6623/-Professional-Drawing-Program.git

# Navigate to project directory
cd -Professional-Drawing-Program

# Install required dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Option 2: Download as ZIP

1. Download the project as a ZIP file from GitHub
2. Extract the ZIP file to your desired location
3. Open terminal/command prompt in the project directory
4. Install dependencies and run:

```bash
# Install required dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Drawing Shapes

1. **Select a shape type** from the control panel (Circle, Ellipse, or Line)
2. **Choose a color** from the color palette
3. **Enter coordinates** for the shape parameters:
   - **Circle**: Center (x, y) and radius
   - **Ellipse**: Center (x, y), horizontal radius (a), and vertical radius (b)
   - **Line**: Start point (x₁, y₁) and end point (x₂, y₂)
4. **Press Enter** or click the Draw button to render the shape

### Coordinate System

- **X-axis**: Horizontal direction (negative left, positive right)
- **Y-axis**: Vertical direction (negative down, positive up)
- **Origin (0, 0)**: Center of the canvas
- Grid spacing adjusts dynamically with zoom level

## Controls

### Mouse
- **Left Click**: Interact with UI elements (buttons, input fields)
- **Mouse Wheel**: 
  - Over control panel: Scroll through options
  - Over canvas: Zoom in/out

### Keyboard Shortcuts
- **Enter**: Draw the current shape
- **Tab**: Navigate between input fields
- **Backspace**: Delete last character in active input field
- **Delete**: Clear all shapes from canvas
- **+/=**: Zoom in
- **-**: Zoom out
- **F5**: Reset zoom to default (100%)
- **F11**: Toggle fullscreen mode
- **Esc**: Exit fullscreen mode

## Color Palette

- 🔴 **Red** - RGB(255, 0, 0)
- 🟢 **Green** - RGB(0, 255, 0)
- 🔵 **Blue** - RGB(0, 0, 255)
- 🟦 **Cyan** - RGB(0, 255, 255)
- 🟪 **Magenta** - RGB(255, 0, 255)
- 🟨 **Yellow** - RGB(255, 255, 0)
- 🟧 **Orange** - RGB(255, 165, 0)
- 🟣 **Purple** - RGB(128, 0, 128)

## Technical Details

### Dependencies
- **Pygame**: Core graphics and UI framework
- See [requirements.txt](requirements.txt) for complete list

### Architecture
The application follows a modular architecture with separation of concerns:
- **MVC Pattern**: Clear separation between models (shapes), views (UI/rendering), and controller (main loop)
- **Factory Pattern**: Dynamic shape creation through shapes_factory
- **Abstraction**: Base shape class for polymorphic rendering
- **Coordinate Transformation**: Screen-space to world-space conversion with zoom support

## Development

### Code Style
- Python PEP 8 conventions
- Type hints where applicable
- Comprehensive docstrings

### Extending the Project
To add a new shape:
1. Create a new class in `shapes/` inheriting from `Shape`
2. Implement the `draw()` method
3. Add the shape to `shapes_factory.py`
4. Update the UI in `ui/panel.py`

## License

This project is created for educational purposes as part of a Computer Graphics course.

## Repository

GitHub: [https://github.com/MohamedAshrf6623/-Professional-Drawing-Program](https://github.com/MohamedAshrf6623/-Professional-Drawing-Program)

## Credits

Developed as a Level 5, Semester 1 Computer Graphics project.

---

**Version**: 1.0  
**Last Updated**: December 2025
