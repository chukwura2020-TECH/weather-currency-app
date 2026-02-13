# gui/components/forecast.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
"""
Forecast display component - now with REAL API data!
🐛 FIXED: Only shows exactly 5 days in forecast
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.weather_api import WeatherAPI
from datetime import datetime

class ForecastPanel(tk.Frame):
    def __init__(self, parent, city="London"):
        super().__init__(parent, bg='white')
        
        self.city = city
        self.api = WeatherAPI()
        self._create_widgets()
        self.update_forecast()  # Fetch real data on startup
    
    def _create_widgets(self):
        """Create forecast list structure"""
        
        # Title
        tk.Label(
            self,
            text="Forecast",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Today/Next tabs
        tabs = tk.Frame(self, bg='white')
        tabs.pack(fill="x", padx=DIMENSIONS['padding'], pady=(0, 10))
        
        tk.Label(
            tabs,
            text="Today",
            bg=COLORS['accent_blue'],
            fg='white',
            font=FONTS['body_bold'],
            padx=15,
            pady=5
        ).pack(side="left", padx=(0, 5))
        
        tk.Label(
            tabs,
            text="Next",
            bg=COLORS['accent_light'],
            fg=COLORS['text_dark'],
            font=FONTS['body'],
            padx=15,
            pady=5
        ).pack(side="left")
        
        # Container for forecast items
        self.forecast_container = tk.Frame(self, bg='white')
        self.forecast_container.pack(fill="both", expand=True)
        
        # Loading message
        self.loading_label = tk.Label(
            self.forecast_container,
            text="Loading forecast...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.loading_label.pack(pady=20)
    
    def update_forecast(self, city=None):
        """Fetch and display real forecast data"""
        if city:
            self.city = city
        
        # Clear existing forecast items
        for widget in self.forecast_container.winfo_children():
            widget.destroy()
        
        # Fetch forecast data
        forecast_data = self.api.get_forecast(self.city)
        
        if forecast_data:
            # 🐛 BUG #1 FIXED: Process forecast to get EXACTLY 5 days
            daily_forecasts = self._process_forecast(forecast_data)
            
            # Display each day - STRICTLY LIMIT TO 5
            for day_data in daily_forecasts[:5]:  # Force limit to 5 days
                self._create_forecast_item(
                    day_data['day'],
                    day_data['icon'],
                    day_data['temp_max'],
                    day_data['temp_min']
                )
        else:
            # Show error
            tk.Label(
                self.forecast_container,
                text="Error loading forecast",
                bg='white',
                fg=COLORS['text_muted'],
                font=FONTS['body']
            ).pack(pady=20)
    
    def _process_forecast(self, forecast_data):
        """
        Process API forecast data into daily summaries
        🐛 FIXED: Returns EXACTLY 5 days, no more
        """
        daily_data = {}
        
        # Group data by day
        for item in forecast_data['list']:
            # Get date
            date = datetime.fromtimestamp(item['dt'])
            day_key = date.strftime('%Y-%m-%d')
            
            if day_key not in daily_data:
                daily_data[day_key] = {
                    'date': date,
                    'temps': [],
                    'conditions': []
                }
            
            daily_data[day_key]['temps'].append(item['main']['temp'])
            daily_data[day_key]['conditions'].append(item['weather'][0]['main'])
        
        # Convert to list format and LIMIT TO 5 DAYS
        result = []
        sorted_days = sorted(daily_data.keys())
        
        # 🐛 CRITICAL FIX: Only process first 5 days
        for day_key in sorted_days[:5]:  # Hard limit to 5 days
            data = daily_data[day_key]
            date = data['date']
            
            # Format day name
            if date.date() == datetime.now().date():
                day_str = "Today"
            else:
                day_str = date.strftime('%a %d %b')
            
            # Get most common condition
            condition = max(set(data['conditions']), key=data['conditions'].count)
            
            result.append({
                'day': day_str,
                'icon': self._get_weather_icon(condition),
                'temp_max': f"{round(max(data['temps']))}°",
                'temp_min': f"{round(min(data['temps']))}°"
            })
        
        # Final safety check - return max 5 items
        return result[:5]
    
    def _create_forecast_item(self, day, icon, high, low):
        """Create a single forecast item"""
        
        item = tk.Frame(self.forecast_container, bg='white')
        item.pack(fill="x", padx=15, pady=3)
        
        # Day
        tk.Label(
            item,
            text=day,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body'],
            width=12,
            anchor="w"
        ).pack(side="left")
        
        # Icon
        tk.Label(
            item,
            text=icon,
            bg='white',
            font=('Segoe UI', 18)
        ).pack(side="left", padx=10)
        
        # Temperatures
        tk.Label(
            item,
            text=high,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(side="right", padx=5)
        
        tk.Label(
            item,
            text=low,
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        ).pack(side="right")
    
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
        }
        return icons.get(condition, "🌤️")