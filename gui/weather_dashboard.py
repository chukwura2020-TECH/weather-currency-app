# gui/weather_dashboard.py
"""
Weather dashboard view with all weather components.
🐛 FIXED: No more lag! Removed loading overlay delays!
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS
from gui.components.search_bar import SearchBar
from gui.components.weather_card import CurrentWeatherCard
from gui.map_gui import WeatherMap
from gui.components.popular_cities import PopularCities
from gui.components.forecast import ForecastPanel
from gui.components.summary_chart import SummaryChart
from api.weather_api import WeatherAPI

class WeatherDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = WeatherAPI()
        self.current_city = "London"
        
        self._create_layout()
        
        # Load initial data WITHOUT blocking UI
        self.after(50, self._initial_load)
    
    def _initial_load(self):
        """Load initial weather data - NO LOADING OVERLAY!"""
        try:
            # Get weather data
            weather_data = self.api.get_current_weather(self.current_city)
            
            if weather_data:
                # Update alert banner with real data
                if hasattr(self.master.master, 'alert_banner'):
                    self.master.master.alert_banner.check_weather_alerts(weather_data)
                
                # Update map with coordinates
                if weather_data.get('coord') and hasattr(self, 'map'):
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    self.map.update_location(self.current_city, lat, lon)
                
                # Update chart
                forecast_data = self.api.get_forecast(self.current_city)
                if forecast_data and hasattr(self, 'chart'):
                    self.chart.update_chart(forecast_data)
        except Exception as e:
            print(f"Initial load error: {e}")
    
    def _create_layout(self):
        """Create the weather dashboard layout"""
        
        # Create canvas for scrolling
        canvas = tk.Canvas(self, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Search bar
        self.search_bar = SearchBar(scrollable_frame, self.on_search)
        self.search_bar.pack(fill="x")
        
        # Current Weather Card
        self.weather_card = CurrentWeatherCard(scrollable_frame, city="London")
        self.weather_card.pack(fill="x", padx=20, pady=(0, 20))
        
        # Two-column layout
        columns = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        columns.pack(fill="both", expand=True, padx=20)
        
        # LEFT COLUMN
        left_col = tk.Frame(columns, bg=COLORS['bg_primary'])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Interactive Map
        self.map = WeatherMap(left_col, city_name="London", lat=51.5074, lon=-0.1278)
        self.map.pack(fill="x", pady=(0, 20))
        
        # Temperature Chart
        self.chart = SummaryChart(left_col)
        self.chart.pack(fill="x")
        
        # RIGHT COLUMN
        right_col = tk.Frame(columns, bg=COLORS['bg_primary'])
        right_col.pack(side="right", fill="both", padx=(10, 0))
        
        # Popular Cities
        self.cities = PopularCities(right_col)
        self.cities.pack(fill="x", pady=(0, 20))
        
        # Forecast
        self.forecast = ForecastPanel(right_col, city="London")
        self.forecast.pack(fill="both", expand=True)
    
    def on_search(self, city):
        """
        Called when user searches for a city
        🐛 FIXED: NO loading overlay = NO lag!
        """
        print(f"Updating weather for: {city}")
        
        self.current_city = city
        
        # Update components directly (no loading overlay blocking!)
        try:
            # Update the weather card
            self.weather_card.update_weather(city)
            
            # Update the forecast
            self.forecast.update_forecast(city)
            
            # Get weather data for alerts and map
            weather_data = self.api.get_current_weather(city)
            
            if weather_data:
                # Update alert banner
                if hasattr(self.master.master, 'alert_banner'):
                    self.master.master.alert_banner.check_weather_alerts(weather_data)
                
                # Update map
                if weather_data.get('coord'):
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    self.map.update_location(city, lat, lon)
                
                # Update chart
                forecast_data = self.api.get_forecast(city)
                if forecast_data:
                    self.chart.update_chart(forecast_data)
        except Exception as e:
            print(f"Search error: {e}")
    
    def update_city(self, city):
        """Update dashboard to show a specific city"""
        self.on_search(city)
    
    def update_colors(self):
        """Update all colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])
        
        # Update all child components
        if hasattr(self, 'weather_card'):
            self._update_widget_colors(self.weather_card)
        if hasattr(self, 'map'):
            self.map.update_colors()
        if hasattr(self, 'chart'):
            self.chart.update_colors()
        if hasattr(self, 'forecast'):
            self._update_widget_colors(self.forecast)
        if hasattr(self, 'cities'):
            self._update_widget_colors(self.cities)
    
    def _update_widget_colors(self, widget):
        """Recursively update widget colors"""
        from gui.styles.theme import COLORS
        
        try:
            if isinstance(widget, tk.Frame):
                if widget.cget('bg') in ['#4A90E2', '#FFFFFF', '#E8F4FD', '#1A202C', '#2D3748']:
                    widget.config(bg=COLORS['bg_card'])
            
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget('bg')
                if current_bg in ['#FFFFFF', '#E8F4FD', '#2D3748']:
                    widget.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])
            
            # Recursively update children
            for child in widget.winfo_children():
                self._update_widget_colors(child)
        except:
            pass