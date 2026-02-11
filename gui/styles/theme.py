# gui/styles/theme.py
"""
Application theme and styling.
"""

# Current theme state
CURRENT_THEME = 'light'

# Light mode colors
LIGHT_COLORS = {
    'bg_primary': '#4A90E2',
    'bg_secondary': '#E8F4FD',
    'sidebar_bg': '#3A7BC8',
    'text_dark': '#2D3748',
    'text_muted': '#718096',
    'text_white': '#FFFFFF',
    'accent_blue': '#4A90E2',
    'accent_light': '#E5E7EB' ,
    'bg_card': '#FFFFFF',
    'border_light': '#E2E8F0',
    'success': '#48BB78',
    'warning': '#ED8936',
    'danger': '#F56565',
}

# Dark mode colors
DARK_COLORS = {
    'bg_primary': '#1A202C',
    'bg_secondary': '#2D3748',
    'sidebar_bg': '#2D3748',
    'text_dark': '#F7FAFC',
    'text_muted': '#A0AEC0',
    'text_white': '#F7FAFC',
    'accent_blue': '#63B3ED',
    'accent_light': '#E5E7EB', 
    'bg_card': '#2D3748',
    'border_light': '#4A5568',
    'success': '#48BB78',
    'warning': '#ED8936',
    'danger': '#F56565',
}

# Active colors (starts with light)
COLORS = LIGHT_COLORS.copy()

# Fonts - ALL possible fonts
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'subheading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 11),
    'body_bold': ('Segoe UI', 11, 'bold'),
    'small': ('Segoe UI', 9),
    'temperature': ('Segoe UI', 48, 'bold'),
    'large': ('Segoe UI', 18, 'bold'),
}

# Dimensions - ALL possible dimensions
DIMENSIONS = {
    'padding': 20,
    'border_radius': 10,
    'window_width': 1400,
    'window_height': 800,
    'sidebar_width': 100,
}

def toggle_theme():
    """Switch between light and dark mode"""
    global CURRENT_THEME, COLORS
    
    if CURRENT_THEME == 'light':
        CURRENT_THEME = 'dark'
        COLORS.update(DARK_COLORS)
    else:
        CURRENT_THEME = 'light'
        COLORS.update(LIGHT_COLORS)
    
    return CURRENT_THEME

def get_current_theme():
    """Get current theme name"""
    return CURRENT_THEME