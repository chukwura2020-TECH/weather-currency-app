# gui/map_gui.py
"""
Map display component.
🐛 FIXED: No more "Access blocked" error!
Uses simple placeholder instead of external map tiles.
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class WeatherMap(tk.Frame):
    """Simple weather map display - No external access needed!"""
    
    def __init__(self, parent, city_name="London", lat=51.5074, lon=-0.1278):
        super().__init__(parent, bg='white', height=250)  # Smaller height
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create simple map display"""
        
        # Header
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Title
        self.title_label = tk.Label(
            header,
            text=f"📍 {self.city_name}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        )
        self.title_label.pack(side="left")
        
        # Map display area - Simple colored background
        map_area = tk.Frame(self, bg='#E8F4FD', relief='solid', bd=1)
        map_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Content container
        content = tk.Frame(map_area, bg='#E8F4FD')
        content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Location icon
        tk.Label(
            content,
            text="🗺️",
            bg='#E8F4FD',
            font=('Segoe UI', 48)
        ).pack()
        
        # City info
        self.city_label = tk.Label(
            content,
            text=self.city_name,
            bg='#E8F4FD',
            fg='#2D3748',
            font=('Segoe UI', 18, 'bold')
        )
        self.city_label.pack(pady=(10, 5))
        
        # Coordinates
        self.coord_label = tk.Label(
            content,
            text=f"Lat: {self.lat:.4f}, Lon: {self.lon:.4f}",
            bg='#E8F4FD',
            fg='#4A5568',
            font=('Segoe UI', 11)
        )
        self.coord_label.pack()
        
        # Info message
        tk.Label(
            content,
            text="💡 Interactive map available in Pro version",
            bg='#E8F4FD',
            fg='#718096',
            font=('Segoe UI', 9),
            justify='center'
        ).pack(pady=(15, 0))
    
    def update_location(self, city_name, lat, lon):
        """Update map to new location"""
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        
        # Update labels
        self.title_label.config(text=f"📍 {city_name}")
        self.city_label.config(text=city_name)
        self.coord_label.config(text=f"Lat: {lat:.4f}, Lon: {lon:.4f}")
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.title_label.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])


class MapPlaceholder(tk.Frame):
    """Simple map placeholder - kept for compatibility"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='white', height=200)
        
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create map placeholder"""
        
        # Title
        tk.Label(
            self,
            text="📍 Location Map",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Map placeholder
        map_frame = tk.Frame(self, bg='#E8F4FD')
        map_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        tk.Label(
            map_frame,
            text="🗺️\n\nLocation tracking active\n💡 Interactive maps coming soon",
            bg='#E8F4FD',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        ).pack(expand=True)