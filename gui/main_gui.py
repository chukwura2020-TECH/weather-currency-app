# gui/main_gui.py
"""
Main application window - with Weather and Currency tabs.
"""
from gui.components.alert_banner import AlertBanner
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS
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
        
        # Alert banner (add right after creating content_frame)
        self.alert_banner = AlertBanner(self.content_frame)
        
        # Load default view (Weather)
        self.current_view = None
        self.switch_view("weather")
        
        #Test alert (remove after testing)
        self.alert_banner.show_alert("Severe Weather Alert: Heavy rain expected!", "warning")


    
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