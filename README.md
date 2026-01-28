# Weather & Currency Dashboard

A modern desktop application built with Python Tkinter for displaying weather forecasts and currency conversion.

## Team Members
-  Chukwura- UI Layout & Map Component
- Milicent - Popular Cities Component  
- Goodness - Forecast Component
- Nwayobuije - Summary Chart Component

## Features
- 🌤️ Current weather display
- 📍 Popular cities weather
- 📅 5-day weather forecast
- 📊 Hourly summary chart
- 🗺️ Map integration (placeholder)
- 🔍 Location search
- 🎨 Modern, responsive UI

## Technologies Used
- Python 3.x
- Tkinter (GUI framework)
- Git/GitHub (version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chukwura2020-TECH/weather-currency-app.git
cd weather-currency-app
```

2. Create virtual environment:
```bash
python -m venv weacur
```

3. Activate virtual environment:
- **Windows:** `weacur\Scripts\activate`
- **Mac/Linux:** `source weacur/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python main.py
```

## Project Structure
```
weather-currency-app/
├── gui/
│   ├── styles/
│   │   └── theme.py              # Color scheme and styling
│   ├── components/
│   │   ├── sidebar.py            # Navigation sidebar
│   │   ├── search_bar.py         # Search input
│   │   ├── weather_card.py       # Current weather display
│   │   ├── popular_cities.py     # Cities list
│   │   ├── forecast.py           # 5-day forecast
│   │   └── summary_chart.py      # Hourly chart
│   ├── main_gui.py               # Main application window
│   └── map_gui.py                # Map placeholder
├── main.py                       # Application entry point
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Current Status
✅ Phase 1-5: UI Complete  
🔄 Phase 6: API Integration (In Progress)  
📅 Phase 7: Currency Converter (Planned)  
📅 Phase 8: Polish & Features (Planned)  
📅 Phase 9: Deployment (Planned)

## Future Enhancements
- [ ] Connect to OpenWeatherMap API for real data
- [ ] Implement currency converter
- [ ] Add weather icons (replace emojis)
- [ ] Add loading animations
- [ ] Save favorite locations
- [ ] Dark mode toggle

## License
Educational project - 2026
