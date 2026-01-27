# gui/components/popular_cities.py
"""
Popular cities panel.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class PopularCities(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create popular cities list"""
        
        # Title
        tk.Label(
            self,
            text="Popular Cities",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Sample cities
        cities = [
            ("Delhi", "☀️", "Sunny Cloady"),
            ("Mumbai", "🌧️", "Scattered Rain"),
            ("Singapore", "🌧️", "Heavy Rain"),
            ("Bangalore", "⚡", "Light Thunder"),
        ]
        
        for city, icon, condition in cities:
            self._create_city_item(city, icon, condition)
    
    def _create_city_item(self, city, icon, condition):
        """Create a single city item"""
        
        item = tk.Frame(self, bg='white')
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
        
        tk.Label(
            info,
            text=city,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold'],
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info,
            text=condition,
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small'],
            anchor="w"
        ).pack(fill="x")