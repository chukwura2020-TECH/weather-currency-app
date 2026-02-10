# gui/main_gui.py
"""
Main application window - with Weather and Currency tabs.
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS
from gui.styles.theme import COLORS      
from gui.components.sidebar import Sidebar
from gui.currency_gui import CurrencyConverter

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather & Currency Dashboard")
        
        # Set window size
        window_width = DIMENSIONS['window_width']
        window_height = DIMENSIONS['window_height']
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Set background color
        self.root.configure(bg=COLORS['bg_primary'])
        
        self._create_layout()
    
    def _create_layout(self):
        """Create the main layout with sidebar and tabbed content"""
        
        # LEFT: Sidebar
        self.sidebar = Sidebar(self.root, self.switch_view)
        self.sidebar.pack(side="left", fill="y")
        
        # RIGHT: Main content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Load default view (Weather)
        self.current_view = None
        self.switch_view("weather")
    
    def switch_view(self, view_name):
        """Switch between different views (Weather, Currency)"""
        
        # Clear current view
        if self.current_view:
            self.current_view.destroy()
        
        # Load new view
        if view_name == "weather":
            # Import here to avoid circular imports
            from gui.weather_dashboard import WeatherDashboard
            self.current_view = WeatherDashboard(self.content_frame)
        elif view_name == "currency":
            self.current_view = CurrencyConverter(self.content_frame)
        else:
            # Placeholder for other views
            self.current_view = tk.Label(
                self.content_frame,
                text=f"{view_name.title()} - Coming Soon",
                bg=COLORS['bg_primary'],
                fg=COLORS['text_white'],
                font=FONTS['title']
            )
        
        self.current_view.pack(fill="both", expand=True)

    def refresh_all_colors(self):
        """Refresh all component colors when theme changes"""
    # Update root background
        self.root.config(bg=COLORS['bg_primary'])
    
    # Recursively update all widgets
        self._update_widget_colors(self.root)

def _update_widget_colors(self, widget):
    """Recursively update widget colors"""
    from gui.styles.theme import COLORS
    
    try:
        # Update common widget types
        if isinstance(widget, tk.Frame):
            if 'bg' in widget.config():
                current_bg = widget.cget('bg')
                # Update if it's using theme colors
                if current_bg in ['#4A90E2', '#FFFFFF', '#E8F4FD']:
                    widget.config(bg=COLORS['bg_primary'])
        
        elif isinstance(widget, tk.Label):
            if 'bg' in widget.config():
                widget.config(bg=COLORS['card_bg'], fg=COLORS['text_dark'])
        
        # Recursively update children
        for child in widget.winfo_children():
            self._update_widget_colors(child)
    except:
        pass