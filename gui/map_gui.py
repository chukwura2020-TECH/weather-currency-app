# gui/map_gui.py
"""
Map display component with REAL weather overlay! 🗺️
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from PIL import Image, ImageTk
import requests
from io import BytesIO
from config import OPENWEATHER_API_KEY

class WeatherMap(tk.Frame):
    """Interactive weather map with layer options"""
    
    def __init__(self, parent, city_name="London", lat=51.5074, lon=-0.1278):
        super().__init__(parent, bg='white', height=300)
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.zoom = 8
        self.current_layer = 'temp_new'  # Default layer
        self.api_key = OPENWEATHER_API_KEY
        
        self.pack_propagate(False)
        
        self._create_widgets()
        self.load_map()
    
    def _create_widgets(self):
        """Create map UI"""
        
        # Header with title and controls
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Title
        self.title_label = tk.Label(
            header,
            text=f"Weather Map - {self.city_name}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        )
        self.title_label.pack(side="left")
        
        # Layer selector
        layer_frame = tk.Frame(header, bg='white')
        layer_frame.pack(side="right")
        
        tk.Label(
            layer_frame,
            text="Layer:",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(side="left", padx=(0, 5))
        
        self.layer_var = tk.StringVar(value='Temperature')
        layer_combo = ttk.Combobox(
            layer_frame,
            textvariable=self.layer_var,
            values=['Temperature', 'Precipitation', 'Clouds', 'Pressure'],
            state='readonly',
            width=12,
            font=FONTS['small']
        )
        layer_combo.pack(side="left")
        layer_combo.bind('<<ComboboxSelected>>', self._on_layer_change)
        
        # Map canvas
        self.map_canvas = tk.Canvas(
            self,
            bg='#E8F4FD',
            highlightthickness=0
        )
        self.map_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Loading label
        self.loading_label = tk.Label(
            self.map_canvas,
            text="Loading map...",
            bg='#E8F4FD',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Zoom controls
        zoom_frame = tk.Frame(self, bg='white')
        zoom_frame.pack(side='bottom', pady=(0, 10))
        
        tk.Button(
            zoom_frame,
            text="−",
            command=self.zoom_out,
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['accent_light'],
            fg=COLORS['text_dark'],
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=2)
        
        tk.Button(
            zoom_frame,
            text="+",
            command=self.zoom_in,
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['accent_light'],
            fg=COLORS['text_dark'],
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=2)
    
    def _on_layer_change(self, event=None):
        """Handle layer selection change"""
        layer_map = {
            'Temperature': 'temp_new',
            'Precipitation': 'precipitation_new',
            'Clouds': 'clouds_new',
            'Pressure': 'pressure_new'
        }
        
        self.current_layer = layer_map.get(self.layer_var.get(), 'temp_new')
        self.load_map()
    
    def load_map(self):
        """Load map image from OpenWeatherMap API"""
        try:
            self.loading_label.config(text="Loading map...")
            self.loading_label.place(relx=0.5, rely=0.5, anchor='center')
            
            # OpenWeatherMap tile API
            # Format: http://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={API key}
            
            # Calculate tile coordinates from lat/lon
            x_tile, y_tile = self._lat_lon_to_tile(self.lat, self.lon, self.zoom)
            
            # Build URL for weather overlay
            tile_url = f"https://tile.openweathermap.org/map/{self.current_layer}/{self.zoom}/{x_tile}/{y_tile}.png?appid={self.api_key}"
            
            # Also get base map tile (for context)
            base_url = f"https://tile.openstreetmap.org/{self.zoom}/{x_tile}/{y_tile}.png"
            
            # Download images
            response_base = requests.get(base_url, timeout=5)
            response_weather = requests.get(tile_url, timeout=5)
            
            if response_base.status_code == 200:
                # Load base map
                img_base = Image.open(BytesIO(response_base.content))
                
                # Overlay weather if available
                if response_weather.status_code == 200:
                    img_weather = Image.open(BytesIO(response_weather.content))
                    # Blend the images
                    img_base = Image.blend(img_base.convert('RGBA'), img_weather.convert('RGBA'), alpha=0.6)
                
                # Resize to fit canvas
                canvas_width = self.map_canvas.winfo_width()
                canvas_height = self.map_canvas.winfo_height()
                
                if canvas_width > 1 and canvas_height > 1:
                    img_base = img_base.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.map_image = ImageTk.PhotoImage(img_base)
                
                # Display on canvas
                self.map_canvas.delete('all')
                self.map_canvas.create_image(0, 0, anchor='nw', image=self.map_image)
                self.loading_label.place_forget()
            else:
                self.loading_label.config(text="❌ Map unavailable")
        
        except Exception as e:
            print(f"Map error: {e}")
            self.loading_label.config(text="❌ Map loading failed\nCheck internet connection")
    
    def _lat_lon_to_tile(self, lat, lon, zoom):
        """Convert latitude/longitude to tile coordinates"""
        import math
        
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x_tile = int((lon + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        
        return x_tile, y_tile
    
    def update_location(self, city_name, lat, lon):
        """Update map to new location"""
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.title_label.config(text=f"Weather Map - {city_name}")
        self.load_map()
    
    def zoom_in(self):
        """Zoom in"""
        if self.zoom < 12:
            self.zoom += 1
            self.load_map()
    
    def zoom_out(self):
        """Zoom out"""
        if self.zoom > 5:
            self.zoom -= 1
            self.load_map()
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.title_label.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])


class MapPlaceholder(tk.Frame):
    """Simple placeholder - kept for compatibility"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='white', height=200)
        
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create map placeholder"""
        
        # Title
        tk.Label(
            self,
            text="Weather Map",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Map placeholder
        tk.Label(
            self,
            text="🗺️\n\nMap view coming soon...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        ).pack(expand=True)