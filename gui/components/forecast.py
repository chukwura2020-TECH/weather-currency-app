# gui/components/forecast.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
"""
Forecast display component - now with REAL API data!
🐛 FIXED: BOTH "Today" and "Next" tabs work!
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
        self.forecast_data = None
        self.current_tab = "Today"
        
        self._create_widgets()
        self.update_forecast()
    
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
        
        # Today/Next tabs - BOTH FUNCTIONAL!
        tabs = tk.Frame(self, bg='white')
        tabs.pack(fill="x", padx=DIMENSIONS['padding'], pady=(0, 10))
        
        self.today_tab = tk.Label(
            tabs,
            text="Today",
            bg=COLORS['accent_blue'],
            fg='white',
            font=FONTS['body_bold'],
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.today_tab.pack(side="left", padx=(0, 5))
        self.today_tab.bind('<Button-1>', lambda e: self._switch_tab("Today"))
        
        self.next_tab = tk.Label(
            tabs,
            text="Next 5 Days",
            bg=COLORS['accent_light'],
            fg=COLORS['text_dark'],
            font=FONTS['body'],
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.next_tab.pack(side="left")
        self.next_tab.bind('<Button-1>', lambda e: self._switch_tab("Next"))
        
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
    
    def _switch_tab(self, tab_name):
        """Switch between Today and Next tabs"""
        print(f"📅 Switching to {tab_name} tab")
        
        self.current_tab = tab_name
        
        # Update tab colors
        if tab_name == "Today":
            self.today_tab.config(bg=COLORS['accent_blue'], fg='white', font=FONTS['body_bold'])
            self.next_tab.config(bg=COLORS['accent_light'], fg=COLORS['text_dark'], font=FONTS['body'])
        else:
            self.today_tab.config(bg=COLORS['accent_light'], fg=COLORS['text_dark'], font=FONTS['body'])
            self.next_tab.config(bg=COLORS['accent_blue'], fg='white', font=FONTS['body_bold'])
        
        # Redraw forecast
        self._display_forecast()
    
    def update_forecast(self, city=None):
        """Fetch and display real forecast data"""
        if city:
            self.city = city
        
        # Clear existing
        for widget in self.forecast_container.winfo_children():
            widget.destroy()
        
        # Fetch forecast data
        self.forecast_data = self.api.get_forecast(self.city)
        
        if self.forecast_data:
            self._display_forecast()
        else:
            tk.Label(
                self.forecast_container,
                text="Error loading forecast",
                bg='white',
                fg=COLORS['text_muted'],
                font=FONTS['body']
            ).pack(pady=20)
    
    def _display_forecast(self):
        """Display forecast based on current tab"""
        # Clear container
        for widget in self.forecast_container.winfo_children():
            widget.destroy()
        
        if not self.forecast_data:
            return
        
        if self.current_tab == "Today":
            self._show_today_forecast()
        else:
            self._show_next_days_forecast()
    
    def _show_today_forecast(self):
        """Show today's hourly forecast"""
        today = datetime.now().date()
        
        hourly_items = []
        for item in self.forecast_data['list']:
            item_date = datetime.fromtimestamp(item['dt']).date()
            if item_date == today:
                hourly_items.append(item)
        
        if not hourly_items:
            hourly_items = self.forecast_data['list'][:8]  # Next 24 hours
        
        for item in hourly_items[:8]:  # Show 8 hours
            time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
            icon = self._get_weather_icon(item['weather'][0]['main'])
            temp = f"{round(item['main']['temp'])}°"
            
            self._create_forecast_item(time, icon, temp, "")
    
    def _show_next_days_forecast(self):
        """Show next 5 days forecast"""
        daily_forecasts = self._process_forecast(self.forecast_data)
        
        for day_data in daily_forecasts[:5]:
            self._create_forecast_item(
                day_data['day'],
                day_data['icon'],
                day_data['temp_max'],
                day_data['temp_min']
            )
    
    def _process_forecast(self, forecast_data):
        """Process API forecast data into daily summaries"""
        daily_data = {}
        
        for item in forecast_data['list']:
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
        
        result = []
        sorted_days = sorted(daily_data.keys())
        
        for day_key in sorted_days[:5]:
            data = daily_data[day_key]
            date = data['date']
            
            if date.date() == datetime.now().date():
                day_str = "Today"
            else:
                day_str = date.strftime('%a %d %b')
            
            condition = max(set(data['conditions']), key=data['conditions'].count)
            
            result.append({
                'day': day_str,
                'icon': self._get_weather_icon(condition),
                'temp_max': f"{round(max(data['temps']))}°",
                'temp_min': f"{round(min(data['temps']))}°"
            })
        
        return result[:5]
    
    def _create_forecast_item(self, day, icon, high, low):
        """Create a single forecast item"""
        
        item = tk.Frame(self.forecast_container, bg='white')
        item.pack(fill="x", padx=15, pady=3)
        
        # Day/Time
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
        
        if low:  # Only show if we have a low temp
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