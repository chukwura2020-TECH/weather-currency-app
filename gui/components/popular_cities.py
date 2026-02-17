# gui/components/popular_cities.py
"""
Popular cities panel - now with REAL API data!
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.weather_api import WeatherAPI

class PopularCities(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self.api = WeatherAPI()
        self._create_widgets()
        self.update_cities()  # Fetch real data on startup
    
    def _create_widgets(self):
        """Create popular cities list"""
        
        # Title
        tk.Label(
            self,
            text="Popular Cities",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Container for city items
        self.cities_container = tk.Frame(self, bg='white')
        self.cities_container.pack(fill="both", expand=True)
        
        # Initially show loading
        self.loading_label = tk.Label(
            self.cities_container,
            text="Loading cities...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.loading_label.pack(pady=20)
    
    def update_cities(self):
        """Fetch and display real weather for popular cities"""
        
        # Clear loading message
        self.loading_label.destroy()
        
        # Cities to fetch
        cities = ["Delhi", "Mumbai", "Singapore", "Bangalore"]
        
        for city in cities:
            weather_data = self.api.get_current_weather(city)
            
            if weather_data:
                temp = round(weather_data['main']['temp'])
                condition = weather_data['weather'][0]['main']
                icon = self._get_weather_icon(condition)
                
                self._create_city_item(city, icon, f"{temp}°C", condition)
            else:
                # Show error for this city
                self._create_city_item(city, "❌", "--°C", "Error")
    
    def _create_city_item(self, city, icon, temp, condition):
        """Create a single city item with real data"""
        
        item = tk.Frame(self.cities_container, bg='white')
        item.pack(fill="x", padx=15, pady=5)
        
        # Icon
        tk.Label(
            item,
            text=icon,
            bg='white',
            font=('Segoe UI', 24)
        ).pack(side="left", padx=(0, 10))
        
        # City info
        info = tk.Frame(item, bg='white')
        info.pack(side="left", fill="x", expand=True)
        
        # City name and temperature
        tk.Label(
            info,
            text=f"{city} - {temp}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold'],
            anchor="w"
        ).pack(fill="x")
        
        # Weather condition
        tk.Label(
            info,
            text=condition,
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small'],
            anchor="w"
        ).pack(fill="x")
    
    def _get_weather_icon(self, condition):
        """Return appropriate emoji for weather condition"""
        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Haze": "🌫️",
        }
        return icons.get(condition, "🌤️")