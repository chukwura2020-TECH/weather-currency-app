# gui/main_gui.py
"""
Main application window with sidebar and weather content.
"""
import tkinter as tk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS  # ← Added FONTS here
from gui.components.sidebar import Sidebar
from gui.components.search_bar import SearchBar
from gui.components.weather_card import CurrentWeatherCard

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        
        # Set window size
        window_width = DIMENSIONS['window_width']
        window_height = DIMENSIONS['window_height']
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Set background color
        self.root.configure(bg=COLORS['bg_primary'])
        
        self._create_layout()
    
    def _create_layout(self):
        """Create the main layout with sidebar and content area"""
        
        # LEFT: Sidebar
        self.sidebar = Sidebar(self.root)
        self.sidebar.pack(side="left", fill="y")
        
        # RIGHT: Main content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Search bar at the top
        self.search_bar = SearchBar(self.content_frame)
        self.search_bar.pack(fill="x")
        
        # Current Weather Card
        self.weather_card = CurrentWeatherCard(self.content_frame)
        self.weather_card.pack(fill="x", padx=20, pady=(0, 20))
        
        # Placeholder for more content below
        placeholder = tk.Label(
            self.content_frame,
            text="More content coming in Phase 5...",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['body']  # ← Now FONTS is imported, so this works!
        )
        placeholder.pack(pady=50)
