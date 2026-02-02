# gui/main_gui.py
"""
Main application window - complete dashboard.
"""
import tkinter as tk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS
from gui.components.sidebar import Sidebar
from gui.components.search_bar import SearchBar
from gui.components.weather_card import CurrentWeatherCard
from gui.map_gui import MapPlaceholder
from gui.components.popular_cities import PopularCities
from gui.components.forecast import ForecastPanel
from gui.components.summary_chart import SummaryChart

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
        """Create the complete dashboard layout"""
        
        # LEFT: Sidebar
        self.sidebar = Sidebar(self.root)
        self.sidebar.pack(side="left", fill="y")
        
        # RIGHT: Main content area with scrolling
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add all components
        
        # Search bar
        # Search bar at the top (with callback)
        self.search_bar = SearchBar(scrollable_frame, self.on_search)
        self.search_bar.pack(fill="x")
        
        # Current Weather Card
        # Current Weather Card (with default city)
        self.weather_card = CurrentWeatherCard(scrollable_frame, city="London")
        self.weather_card.pack(fill="x", padx=20, pady=(0, 20))
        
        # Two-column layout
        columns = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        columns.pack(fill="both", expand=True, padx=20)
        
        # LEFT COLUMN
        left_col = tk.Frame(columns, bg=COLORS['bg_primary'])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Map
        self.map = MapPlaceholder(left_col)
        self.map.pack(fill="x", pady=(0, 20))
        
        # Summary Chart
        self.chart = SummaryChart(left_col)
        self.chart.pack(fill="x")
        
        # RIGHT COLUMN
        right_col = tk.Frame(columns, bg=COLORS['bg_primary'])
        right_col.pack(side="right", fill="both", padx=(10, 0))
        
        # Popular Cities
        self.cities = PopularCities(right_col)
        self.cities.pack(fill="x", pady=(0, 20))
        

        # Forecast (with default city)
        self.forecast = ForecastPanel(right_col, city="London")
        self.forecast.pack(fill="both", expand=True)

    def on_search(self, city):
        """Called when user searches for a city"""
        print(f"Updating weather for: {city}")
        
        # Update the weather card with new city
        self.weather_card.update_weather(city)
        
        # Update the forecast with new city
        self.forecast.update_forecast(city)