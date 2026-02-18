# gui/components/popular_cities.py
"""
Popular cities panel - now with REAL API data!
🔄 UPDATED: Random world cities shown on every refresh!
"""
import tkinter as tk
import random
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.weather_api import WeatherAPI

class PopularCities(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self.api = WeatherAPI()

        # Large pool of cities from around the world
        self.all_cities = [
            # Europe
            "London", "Paris", "Berlin", "Madrid", "Rome",
            "Amsterdam", "Vienna", "Stockholm", "Oslo", "Zurich",
            "Brussels", "Lisbon", "Athens", "Prague", "Warsaw",
            # Americas
            "New York", "Los Angeles", "Toronto", "Chicago", "Miami",
            "Mexico City", "Sao Paulo", "Buenos Aires", "Lima", "Bogota",
            "Vancouver", "Houston", "Montreal", "Santiago", "Havana",
            # Asia
            "Tokyo", "Beijing", "Shanghai", "Seoul", "Bangkok",
            "Delhi", "Mumbai", "Singapore", "Bangalore", "Karachi",
            "Dhaka", "Osaka", "Kuala Lumpur", "Jakarta", "Manila",
            # Africa
            "Cairo", "Lagos", "Nairobi", "Casablanca", "Accra",
            "Johannesburg", "Addis Ababa", "Dar es Salaam", "Tunis", "Dakar",
            # Middle East
            "Dubai", "Riyadh", "Istanbul", "Tehran", "Baghdad",
            "Doha", "Kuwait City", "Beirut", "Amman", "Muscat",
            # Oceania
            "Sydney", "Melbourne", "Auckland", "Brisbane", "Perth",
        ]

        self._create_widgets()
        self.update_cities()  # Fetch real data on startup
    
    def _create_widgets(self):
        """Create popular cities list"""

        # Header row with title and refresh button
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))

        tk.Label(
            header,
            text="Popular Cities",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Refresh button
        refresh_btn = tk.Button(
            header,
            text="🔄",
            bg='white',
            fg=COLORS['text_dark'],
            font=('Segoe UI', 12),
            bd=0,
            cursor="hand2",
            activebackground='#EDF2F7',
            command=self._refresh_cities
        )
        refresh_btn.pack(side="right")
        
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
    
    def _refresh_cities(self):
        """Clear current cities and load a new random set"""
        # Clear all existing city items
        for widget in self.cities_container.winfo_children():
            widget.destroy()

        # Show loading message
        self.loading_label = tk.Label(
            self.cities_container,
            text="Loading cities...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.loading_label.pack(pady=20)
        self.update_idletasks()

        # Load new random cities
        self.update_cities()

    def update_cities(self):
        """Fetch and display real weather for 4 random world cities"""

        # Destroy loading label if it still exists
        for widget in self.cities_container.winfo_children():
            widget.destroy()

        # Pick 4 random cities from the global pool
        selected_cities = random.sample(self.all_cities, 4)
        
        for city in selected_cities:
            weather_data = self.api.get_current_weather(city)
            
            if weather_data:
                temp = round(weather_data['main']['temp'])
                condition = weather_data['weather'][0]['main']
                icon = self._get_weather_icon(condition)
                
                self._create_city_item(city, icon, f"{temp}°C", condition)
            else:
                # Show error for this city
                self._create_city_item(city, "❌", "--°C", "Unavailable")
    
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
            "Fog": "🌫️",
            "Dust": "🌪️",
            "Sand": "🌪️",
            "Smoke": "🌫️",
        }
        return icons.get(condition, "🌤️")