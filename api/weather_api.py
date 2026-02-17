# api/weather_api.py
"""
Weather API integration using OpenWeatherMap.
"""
import requests
from config import OPENWEATHER_API_KEY

class WeatherAPI:
    """Handles all weather data fetching from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city):
        """
        Get current weather for a city.
        
        Args:
            city (str): City name (e.g., "London", "New York")
            
        Returns:
            dict: Weather data or None if error
        """
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Celsius
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")
            return None
    
    def get_forecast(self, city, days=5):
        """
        Get weather forecast for a city.
        
        Args:
            city (str): City name
            days (int): Number of days (max 5 for free tier)
            
        Returns:
            dict: Forecast data or None if error
        """
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast for {city}: {e}")
            return None