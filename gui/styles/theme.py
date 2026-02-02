# gui/styles/theme.py
"""
Theme configuration for the Weather Dashboard.
Contains all colors, fonts, and dimensions used throughout the app.
"""

# ============= COLORS =============
COLORS = {
    # Main background colors
    'bg_primary': '#5B9BD5',      # Blue background (like in the image)
    'bg_secondary': '#4A7BA7',    # Slightly darker blue
    'bg_card': '#FFFFFF',         # White for cards/panels
    'bg_sidebar': '#2E5090',      # Dark blue for sidebar
    
    # Text colors
    'text_white': '#FFFFFF',      # White text
    'text_dark': '#2C3E50',       # Dark text for white backgrounds
    'text_muted': '#95A5A6',      # Gray text for less important info
    
    # Accent colors
    'accent_blue': '#3498DB',
    'accent_light': '#E8F4F8',
    
    # Border colors
    'border_light': '#E1E8ED',    # Light gray border
}

# ============= FONTS =============
FONTS = {
    'title': ('Segoe UI', 28, 'bold'),           # Large titles
    'heading': ('Segoe UI', 16, 'bold'),         # Section headings
    'subheading': ('Segoe UI', 14, 'bold'),      # Subheadings
    'body': ('Segoe UI', 11),                    # Normal text
    'body_bold': ('Segoe UI', 11, 'bold'),       # Bold text
    'temperature': ('Segoe UI', 48, 'bold'),     # Big temperature number
    'small': ('Segoe UI', 9),                    # Small text
}

# ============= DIMENSIONS =============
DIMENSIONS = {
    'sidebar_width': 80,          # Sidebar width in pixels
    'window_width': 1280,         # Default window width
    'window_height': 720,         # Default window height
    'padding': 20,                # Standard padding
}