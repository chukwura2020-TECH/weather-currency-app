# gui/components/weather_card.py
"""
Current weather display card - now with REAL API data!
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.weather_api import WeatherAPI
from gui.components.loading import LoadingSpinner 

class CurrentWeatherCard(tk.Frame):
    """Large card displaying current weather conditions from API"""
    
    def __init__(self, parent, city="London"):
        super().__init__(parent, bg='white', relief="flat", bd=0)
        
        # Store city and API FIRST before creating widgets
        self.city = city
        self.api = WeatherAPI()
        
        # Setup spinner
        self.spinner = LoadingSpinner(self, size=60, bg=COLORS['bg_card'])
        self.spinner.place(relx=0.5, rely=0.5, anchor='center')
        self.spinner.pack_forget()
        
        # Add visual depth
        self.config(highlightbackground=COLORS['border_light'], highlightthickness=1)
        
        self._create_widgets()
        self.update_weather()  # Fetch real data on startup

    def show_loading(self):
        """Show loading spinner"""
        self.spinner.pack(pady=100)
        self.spinner.start()

    def hide_loading(self):
        """Hide loading spinner"""
        self.spinner.stop()
        self.spinner.pack_forget()
    
    def _create_widgets(self):
        """Create the weather card layout"""
        
        # Padding frame
        self.content = tk.Frame(self, bg='white')
        self.content.pack(fill="both", expand=True, padx=DIMENSIONS['padding'], 
                         pady=DIMENSIONS['padding'])
        
        # TOP: City name and date
        self.header = tk.Frame(self.content, bg='white')
        self.header.pack(fill="x", pady=(0, 20))
        
        self.city_label = tk.Label(
            self.header,
            text="Loading...",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['title']
        )
        self.city_label.pack(side="left")
        
        self.date_label = tk.Label(
            self.header,
            text="",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.date_label.pack(side="right", pady=5)
        
        # MIDDLE: Weather icon and temperature
        self.main_section = tk.Frame(self.content, bg='white')
        self.main_section.pack(fill="x", pady=20)
        
        # Weather icon
        self.icon_label = tk.Label(
            self.main_section,
            text="🌤️",
            bg='white',
            font=('Segoe UI', 80)
        )
        self.icon_label.pack(side="left", padx=(0, 30))
        
        # Temperature and description
        temp_frame = tk.Frame(self.main_section, bg='white')
        temp_frame.pack(side="left")
        
        self.temp_label = tk.Label(
            temp_frame,
            text="--°C",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['temperature']
        )
        self.temp_label.pack(anchor="w")
        
        self.desc_label = tk.Label(
            temp_frame,
            text="Loading weather...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['subheading']
        )
        self.desc_label.pack(anchor="w")
        
        # BOTTOM: Weather details grid
        self.details_frame = tk.Frame(self.content, bg='white')
        self.details_frame.pack(fill="x", pady=(20, 0))
        
        # Create detail labels (will be updated with real data)
        self.detail_labels = {}
        details = [
            ("humidity", "💧 Humidity", "--"),
            ("wind", "💨 Wind Speed", "--"),
            ("feels_like", "🌡️ Feels Like", "--"),
            ("pressure", "⏲️ Pressure", "--"),
        ]
        
        for i, (key, label, value) in enumerate(details):
            detail_frame = tk.Frame(self.details_frame, bg='white')
            detail_frame.grid(row=0, column=i, padx=20, sticky="w")
            
            tk.Label(
                detail_frame,
                text=label,
                bg='white',
                fg=COLORS['text_muted'],
                font=FONTS['body']
            ).pack(anchor="w")
            
            value_label = tk.Label(
                detail_frame,
                text=value,
                bg='white',
                fg=COLORS['text_dark'],
                font=FONTS['body_bold']
            )
            value_label.pack(anchor="w")
            self.detail_labels[key] = value_label
    
    def update_weather(self, city=None):
        """Fetch and display real weather data from API"""
        if city:
            self.city = city
        
        # Fetch weather data
        weather_data = self.api.get_current_weather(self.city)
        
        if weather_data:
            # Update city name
            self.city_label.config(text=weather_data['name'])
            
            # Update temperature
            temp = round(weather_data['main']['temp'])
            self.temp_label.config(text=f"{temp}°C")
            
            # Update description
            description = weather_data['weather'][0]['description'].title()
            self.desc_label.config(text=description)
            
            # Update weather icon based on condition
            icon = self._get_weather_icon(weather_data['weather'][0]['main'])
            self.icon_label.config(text=icon)
            
            # Update details
            self.detail_labels['humidity'].config(text=f"{weather_data['main']['humidity']}%")
            self.detail_labels['wind'].config(text=f"{weather_data['wind']['speed']} m/s")
            self.detail_labels['feels_like'].config(text=f"{round(weather_data['main']['feels_like'])}°C")
            self.detail_labels['pressure'].config(text=f"{weather_data['main']['pressure']} hPa")
            
            # Update timestamp
            from datetime import datetime
            now = datetime.now().strftime("%A, %H:%M")
            self.date_label.config(text=now)
        else:
            # Show error if API fails
            self.city_label.config(text="Error loading weather")
            self.desc_label.config(text="Please check your connection")
    
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
            "Fog": "🌫️",
        }
        return icons.get(condition, "🌤️")