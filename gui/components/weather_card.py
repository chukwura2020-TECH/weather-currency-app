# gui/components/weather_card.py
"""
Current weather display card.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class CurrentWeatherCard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the weather card layout"""
        
        # Padding container
        container = tk.Frame(self, bg='white')
        container.pack(fill="both", expand=True, padx=DIMENSIONS['padding'], 
                      pady=DIMENSIONS['padding'])
        
        # Header: "Current Weather" + time
        header = tk.Frame(container, bg='white')
        header.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            header,
            text="Current Weather",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(side="left")
        
        tk.Label(
            header,
            text="12 & PM",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        ).pack(side="right")
        
        # Main section: Icon + Temperature
        main_section = tk.Frame(container, bg='white')
        main_section.pack(fill="x", pady=20)
        
        # Weather icon (large emoji for now)
        icon_label = tk.Label(
            main_section,
            text="🌧️",
            bg='white',
            font=('Segoe UI', 72)
        )
        icon_label.pack(side="left", padx=(0, 30))
        
        # Temperature and description
        temp_frame = tk.Frame(main_section, bg='white')
        temp_frame.pack(side="left", anchor="w")
        
        tk.Label(
            temp_frame,
            text="24°C",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['temperature']
        ).pack(anchor="w")
        
        tk.Label(
            temp_frame,
            text="Heavy Rain",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['heading']
        ).pack(anchor="w")
        
        # Weather details (bottom section)
        details_frame = tk.Frame(container, bg='white')
        details_frame.pack(fill="x", pady=(20, 0))
        
        details = [
            ("💧", "97%"),
            ("🌡️", "15 km/h"),
            ("💨", "4%"),
            ("⭕", "1013 HPa"),
        ]
        
        for i, (icon, value) in enumerate(details):
            detail_col = tk.Frame(details_frame, bg='white')
            detail_col.grid(row=0, column=i, padx=15, sticky="w")
            
            tk.Label(
                detail_col,
                text=icon,
                bg='white',
                font=('Segoe UI', 20)
            ).pack()
            
            tk.Label(
                detail_col,
                text=value,
                bg='white',
                fg=COLORS['text_dark'],
                font=FONTS['body_bold']
            ).pack()