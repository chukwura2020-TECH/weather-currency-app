# test_api.py
"""Quick test of the Weather API"""
from api.weather_api import WeatherAPI

def test_weather_api():
    api = WeatherAPI()
    
    # Test current weather
    print("Testing current weather for London...")
    weather = api.get_current_weather("London")
    
    if weather:
        print(f"✅ Success! Temperature in London: {weather['main']['temp']}°C")
        print(f"   Condition: {weather['weather'][0]['description']}")
    else:
        print("❌ Failed to fetch weather")
    
    # Test forecast
    print("\nTesting forecast for New York...")
    forecast = api.get_forecast("New York")
    
    if forecast:
        print(f"✅ Success! Got {len(forecast['list'])} forecast entries")
    else:
        print("❌ Failed to fetch forecast")

if __name__ == "__main__":
    test_weather_api()