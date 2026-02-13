# gui/styles/theme.py
"""
Application theme and styling.
NOW WITH DARK MODE SUPPORT! 🌙
"""

# Current theme state
_current_theme = "light"

# Light Mode Colors
LIGHT_COLORS = {
    'bg_primary': '#4A90E2',      # Main blue background
    'bg_secondary': '#E8F4FD',    # Light blue
    'bg_card': '#FFFFFF',         # White cards
    'card_bg': '#FFFFFF',         # Card background
    'text_dark': '#2D3748',       # Dark text
    'text_white': '#FFFFFF',      # White text
    'text_muted': '#718096',      # Gray text
    'accent_blue': '#4A90E2',     # Blue accent
    'accent_light': '#E8F4FD',    # Light blue accent
    'border_light': '#E2E8F0',    # Light border
}

# Dark Mode Colors
DARK_COLORS = {
    'bg_primary': '#1A202C',      # Dark blue-gray
    'bg_secondary': '#2D3748',    # Darker gray
    'bg_card': '#2D3748',         # Dark card
    'card_bg': '#2D3748',         # Card background
    'text_dark': '#E2E8F0',       # Light text (reversed)
    'text_white': '#FFFFFF',      # White text
    'text_muted': '#A0AEC0',      # Light gray text
    'accent_blue': '#63B3ED',     # Lighter blue for dark mode
    'accent_light': '#4A5568',    # Dark gray accent
    'border_light': '#4A5568',    # Dark border
}

# Start with light mode
COLORS = LIGHT_COLORS.copy()

# Dimensions (same for both themes)
DIMENSIONS = {
    'window_width': 1400,
    'window_height': 800,
    'padding': 20,
    'card_padding': 15,
}

# Fonts (same for both themes)
FONTS = {
    'title': ('Segoe UI', 32, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 16),
    'body': ('Segoe UI', 13),
    'body_bold': ('Segoe UI', 13, 'bold'),
    'small': ('Segoe UI', 11),
    'temperature': ('Segoe UI', 48, 'bold'),
}

def toggle_theme():
    """
    Toggle between light and dark mode.
    
    Returns:
        str: New theme name ('light' or 'dark')
    """
    global _current_theme, COLORS
    
    if _current_theme == "light":
        _current_theme = "dark"
        COLORS.clear()
        COLORS.update(DARK_COLORS)
    else:
        _current_theme = "light"
        COLORS.clear()
        COLORS.update(LIGHT_COLORS)
    
    return _current_theme

def get_current_theme():
    """Get the current theme name."""
    return _current_theme

def is_dark_mode():
    """Check if dark mode is active."""
    return _current_theme == "dark"