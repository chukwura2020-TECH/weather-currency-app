# Weather & Currency Dashboard - User Guide

## Installation

### Option 1: Run the Executable (Windows - No Python Required)

1. Download `WeatherCurrencyDashboard.exe` from the [Releases page]
2. Download `config.template.py` 
3. Rename `config.template.py` to `config.py`
4. Open `config.py` and add your API keys:
   - Get free OpenWeatherMap key: https://openweathermap.org/api
   - Get free Currency API key: https://www.exchangerate-api.com/
5. Place `config.py` in the same folder as the .exe
6. Double-click `WeatherCurrencyDashboard.exe` to run

### Option 2: Run from Source (Requires Python 3.8+)

1. Clone the repository:
# bash
   git clone https://github.com/chukwura2020-TECH/weather-currency-app.git
   cd weather-currency-app


2. Create virtual environment:
# bash
   python -m venv weacur
   weacur\Scripts\activate  # Windows
   source weacur/bin/activate  # Mac/Linux


3. Install dependencies:
# bash
   pip install -r requirements.txt


4. Create `config.py` and add API keys

5. Run:
# bash
   python main.py


## How to Use

### Weather Dashboard

1. **Search for Cities**
   - Click the search bar at the top
   - Type a city name (e.g., "Paris", "Tokyo")
   - Press Enter
   - Weather updates automatically

2. **View Current Weather**
   - See temperature, humidity, wind speed
   - Weather condition with icon
   - Feels like temperature

3. **Check Forecast**
   - View 5-day forecast on the right panel
   - See high/low temperatures
   - Weather conditions for each day

4. **Popular Cities**
   - Quick view of weather in major cities
   - Click to see more details

### Currency Converter

1. **Switch to Currency Tab**
   - Click the 💱 icon in the sidebar

2. **Convert Currency**
   - Enter amount
   - Select "From" currency
   - Select "To" currency
   - Click "Convert"

3. **Quick Swap**
   - Click "⇅ Swap" to reverse currencies

4. **View History**
   - See recent conversions below
   - Review exchange rates

5. **Export History**
   - Click "Export" to save as CSV (if feature is enabled)

## Troubleshooting

### App won't start
- Make sure `config.py` is in the same folder as the .exe
- Check that API keys are correctly entered in `config.py`
- Verify internet connection

### Weather not loading
- Check internet connection
- Verify OpenWeatherMap API key is valid
- Try searching for a different city

### Currency not converting
- Check internet connection
- Verify Currency API key is valid
- Make sure you selected valid currency codes

## Support

For issues or questions:
- GitHub Issues: [Project Issues Page]
- Email: [Your Email]

## Credits

Created by:
- Victor
- Millicente
- Goodness
- Ekene

Powered by:
- OpenWeatherMap API
- ExchangeRate-API