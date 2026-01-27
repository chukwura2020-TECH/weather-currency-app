# gui/components/forecast.py
"""
Forecast display component.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class ForecastPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create forecast list"""
        
        # Title
        tk.Label(
            self,
            text="Forecast",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Today/Next tabs (simplified)
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
        
        # Sample forecast days
        days = [
            ("Today", "☁️", "24°", "23°"),
            ("Thu 4Mar", "🌤️", "23°", "23°"),
            ("Fri 22 Mar", "🌧️", "22°", "18°"),
            ("Sat 26 Mar", "🌧️", "21°", "18°"),
            ("Next Sun", "⛅", "19°", "18°"),
        ]
        
        for day, icon, high, low in days:
            self._create_forecast_item(day, icon, high, low)
    
    def _create_forecast_item(self, day, icon, high, low):
        """Create a single forecast item"""
        
        item = tk.Frame(self, bg='white')
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
            text=f"{high}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(side="right", padx=5)
        
        tk.Label(
            item,
            text=f"{low}",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        ).pack(side="right")