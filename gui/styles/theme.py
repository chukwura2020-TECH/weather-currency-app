# gui/styles/theme.py
"""
Application theme and styling.
🐛 FIXED: Bold colors (never faint!)
🐛 FIXED: Uniform dark mode colors
🐛 FIXED: Better contrast everywhere
"""

# Current theme state
_current_theme = "light"

# Light Mode Colors - BOLD AND CLEAR!
LIGHT_COLORS = {
    'bg_primary': '#4A90E2',      # Bright blue background
    'bg_secondary': '#E8F4FD',    # Light blue
    'bg_card': '#FFFFFF',         # Pure white cards
    'card_bg': '#FFFFFF',         # Card background
    'text_dark': '#1A202C',       # VERY dark text (not faint!)
    'text_white': '#FFFFFF',      # Pure white text
    'text_muted': '#4A5568',      # Medium gray (not too faint!)
    'accent_blue': '#4A90E2',     # Bright blue
    'accent_light': '#E8F4FD',    # Light blue
    'border_light': '#CBD5E0',    # Visible border
}

# Dark Mode Colors - BOLD AND UNIFORM!
DARK_COLORS = {
    'bg_primary': '#1A202C',      # Dark blue-gray (uniform!)
    'bg_secondary': '#2D3748',    # Slightly lighter gray
    'bg_card': '#2D3748',         # Same as secondary (uniform!)
    'card_bg': '#2D3748',         # Card background (uniform!)
    'text_dark': '#F7FAFC',       # BRIGHT white text (not faint!)
    'text_white': '#FFFFFF',      # Pure white
    'text_muted': '#CBD5E0',      # Light gray (visible in dark!)
    'accent_blue': '#63B3ED',     # Bright blue for dark mode
    'accent_light': '#4A5568',    # Dark accent
    'border_light': '#4A5568',    # Visible dark border
}

# Start with light mode
COLORS = LIGHT_COLORS.copy()

# Dimensions
DIMENSIONS = {
    'window_width': 1400,
    'window_height': 800,
    'padding': 20,
    'card_padding': 15,
}

# Fonts
FONTS = {
    'title': ('Segoe UI', 28, 'bold'),  # Slightly smaller
    'heading': ('Segoe UI', 16, 'bold'),
    'subheading': ('Segoe UI', 14),
    'body': ('Segoe UI', 12),
    'body_bold': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 10),
    'temperature': ('Segoe UI', 42, 'bold'),  # Smaller
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
    
    print(f"Theme switched to: {_current_theme}")
    print(f"Colors now: {COLORS}")
    
    return _current_theme

def get_current_theme():
    """Get the current theme name."""
    return _current_theme

def is_dark_mode():
    """Check if dark mode is active."""
    return _current_theme == "dark"