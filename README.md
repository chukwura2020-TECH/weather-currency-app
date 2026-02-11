# Weather & Currency Dashboard

A modern desktop application built with Python Tkinter for real-time weather forecasts and currency conversion.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### Weather Dashboard
- 🌤️ **Real-time weather data** - Current conditions for any city worldwide
- 📍 **Popular cities display** - Quick view of weather in major cities
- 📅 **5-day forecast** - Detailed weather predictions
- 🔍 **City search** - Find weather for any location
- 🗺️ **Map integration** - Visual weather map (placeholder)
- 📊 **Hourly summary** - Temperature trends throughout the day
- 🎨 **Weather icons** - Beautiful PNG icons for weather conditions
- ⏳ **Loading animations** - Smooth loading spinners

### Currency Converter
- 💱 **Real-time exchange rates** - Convert between 40+ currencies
- 🔄 **Quick swap** - Instantly reverse currency pairs
- 📜 **Conversion history** - Track your recent conversions
- 💾 **Export to CSV** - Save conversion history (optional feature)

### User Interface
- 🎯 **Tab switching** - Easy navigation between Weather and Currency
- 📱 **Responsive design** - Clean, modern interface
- 🌙 **Dark mode** - Eye-friendly theme toggle (if implemented)
- ⭐ **Favorite cities** - Save frequently checked locations (if implemented)

## 📸 Screenshots

[Add screenshots here]

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for API calls)

### Quick Start

1. **Clone the repository**
```bash
   git clone https://github.com/chukwura2020-TECH/weather-currency-app.git
   cd weather-currency-app
```

2. **Create virtual environment**
```bash
   python -m venv weacur
```

3. **Activate virtual environment**
   - **Windows:**
```bash
     weacur\Scripts\activate
```
   - **Mac/Linux:**
```bash
     source weacur/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Set up API keys**
   
   Create a `config.py` file in the project root:
```python
   # config.py
   OPENWEATHER_API_KEY = "your_openweather_api_key_here"
   CURRENCY_API_KEY = "your_currency_api_key_here"
```

   Get free API keys:
   - OpenWeatherMap: https://openweathermap.org/api
   - Currency API: https://www.exchangerate-api.com/

6. **Run the application**
```bash
   python main.py
```

## 📦 Requirements
```
requests==2.31.0
Pillow==10.0.0
```

Install all requirements:
```bash
pip install -r requirements.txt
```

## 🏗️ Project Structure
```
weather-currency-app/
├── api/
│   ├── __init__.py
│   ├── weather_api.py          # OpenWeatherMap API integration
│   └── currency_api.py         # Currency exchange API integration
├── gui/
│   ├── styles/
│   │   └── theme.py            # Color scheme and styling
│   ├── components/
│   │   ├── sidebar.py          # Navigation sidebar
│   │   ├── search_bar.py       # Search input component
│   │   ├── weather_card.py     # Current weather display
│   │   ├── popular_cities.py   # Popular cities panel
│   │   ├── forecast.py         # 5-day forecast component
│   │   ├── summary_chart.py    # Hourly weather chart
│   │   ├── conversion_history.py  # Currency history
│   │   └── loading.py          # Loading spinner
│   ├── main_gui.py             # Main application window
│   ├── weather_dashboard.py    # Weather view
│   └── currency_gui.py         # Currency converter view
├── assets/
│   └── icons/
│       └── weather_icon/       # Weather PNG icons
├── main.py                     # Application entry point
├── config.py                   # API keys (not in git)
├── config.template.py          # Template for API keys
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 💻 Usage

### Weather Dashboard

1. **Search for a city:**
   - Click the search bar
   - Type city name (e.g., "London", "Tokyo", "New York")
   - Press Enter
   - Weather updates automatically

2. **View weather details:**
   - Current temperature and conditions
   - Humidity, wind speed, pressure
   - 5-day forecast
   - Popular cities weather

### Currency Converter

1. **Switch to currency tab:**
   - Click 💱 icon in sidebar

2. **Convert currency:**
   - Enter amount
   - Select "From" currency
   - Select "To" currency
   - Click "Convert"

3. **Swap currencies:**
   - Click "⇅ Swap" button

## 🛠️ Technologies Used

- **Python 3.x** - Programming language
- **Tkinter** - GUI framework
- **Requests** - HTTP library for API calls
- **Pillow (PIL)** - Image processing for weather icons
- **OpenWeatherMap API** - Weather data
- **ExchangeRate-API** - Currency exchange rates

## 👥 Team

- **Chukwura** - UI Layout & Map Component
- **Milicent** - Popular Cities Component
- **Goodness** - Forecast Component
- **Ekene** - Summary Chart Component

## 🤝 Contributing

This is an educational project. Feel free to fork and improve!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Map integration is currently a placeholder
- Some features may require additional API quota for heavy usage

## 📝 Future Enhancements

- [ ] Interactive weather maps
- [ ] Weather alerts and notifications
- [ ] Historical weather data charts
- [ ] Cryptocurrency support
- [ ] Offline mode
- [ ] Mobile responsive design

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- ExchangeRate-API for currency data
- Erik Flowers for Weather Icons

## 📧 Contact

Project Link: https://github.com/chukwura2020-TECH/weather-currency-app

---

**Built with ❤️ by Team Weaher-Currency**