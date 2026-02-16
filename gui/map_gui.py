# gui/map_gui.py
"""
Map display component with BEAUTIFUL EARTH ANIMATION!
🐛 ENHANCED: Beautiful animated earth with zoom to location!
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
import math

class WeatherMap(tk.Frame):
    """Beautiful animated earth map!"""
    
    def __init__(self, parent, city_name="London", lat=51.5074, lon=-0.1278):
        super().__init__(parent, bg='white', height=300)
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.animation_step = 0
        self.is_animating = False
        self.zoom_level = 0
        
        self.pack_propagate(False)
        
        self._create_widgets()
        self._start_animation()
    
    def _create_widgets(self):
        """Create beautiful map display"""
        
        # Header
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Title
        self.title_label = tk.Label(
            header,
            text=f"🌍 {self.city_name}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        )
        self.title_label.pack(side="left")
        
        # Zoom indicator
        self.zoom_label = tk.Label(
            header,
            text="🔍 Global View",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small']
        )
        self.zoom_label.pack(side="right")
        
        # Canvas for animated earth
        self.map_canvas = tk.Canvas(
            self,
            bg='#1a1a2e',  # Dark space background
            highlightthickness=0
        )
        self.map_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Bind resize event
        self.map_canvas.bind('<Configure>', self._on_resize)
        
        # Draw initial earth
        self._draw_earth()
    
    def _draw_earth(self):
        """Draw beautiful animated earth"""
        self.map_canvas.delete('all')
        
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
        
        center_x = width // 2
        center_y = height // 2
        
        # Stars in background
        import random
        random.seed(42)
        for i in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 2)
            self.map_canvas.create_oval(
                x, y, x+size, y+size,
                fill='white', outline='white'
            )
        
        # Earth size based on zoom
        base_radius = min(width, height) // 3
        earth_radius = base_radius + (self.zoom_level * 5)
        
        # Outer glow
        glow_radius = earth_radius + 10
        self.map_canvas.create_oval(
            center_x - glow_radius, center_y - glow_radius,
            center_x + glow_radius, center_y + glow_radius,
            fill='#4A90E2', outline='',
            tags='glow'
        )
        
        # Earth sphere
        self.map_canvas.create_oval(
            center_x - earth_radius, center_y - earth_radius,
            center_x + earth_radius, center_y + earth_radius,
            fill='#2D5F8D', outline='#1E3A5F', width=2,
            tags='earth'
        )
        
        # Continents (simplified shapes that rotate)
        self._draw_continents(center_x, center_y, earth_radius)
        
        # Location marker
        self._draw_location_marker(center_x, center_y, earth_radius)
        
        # City info overlay
        self._draw_info_overlay(center_x, center_y, earth_radius)
    
    def _draw_continents(self, cx, cy, radius):
        """Draw simplified animated continents"""
        # Rotation based on animation step
        rotation = (self.animation_step * 2) % 360
        
        # Simplified continent shapes (North America, Europe, Africa, Asia)
        continents = [
            # North America
            {'angle': 120 + rotation, 'size': 0.3, 'color': '#4CAF50'},
            # Europe
            {'angle': 180 + rotation, 'size': 0.2, 'color': '#66BB6A'},
            # Africa  
            {'angle': 200 + rotation, 'size': 0.25, 'color': '#81C784'},
            # Asia
            {'angle': 240 + rotation, 'size': 0.4, 'color': '#4CAF50'},
        ]
        
        for cont in continents:
            angle_rad = math.radians(cont['angle'])
            x = cx + radius * 0.6 * math.cos(angle_rad)
            y = cy + radius * 0.6 * math.sin(angle_rad)
            size = radius * cont['size']
            
            self.map_canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=cont['color'], outline='',
                tags='continent'
            )
    
    def _draw_location_marker(self, cx, cy, radius):
        """Draw location marker with pulse effect"""
        # Calculate marker position based on lat/lon
        lat_rad = math.radians(self.lat)
        lon_rad = math.radians(self.lon + (self.animation_step * 0.5) % 360)
        
        x = cx + radius * 0.7 * math.cos(lon_rad) * math.cos(lat_rad)
        y = cy + radius * 0.7 * math.sin(lat_rad)
        
        # Pulse effect
        pulse_size = 8 + math.sin(self.animation_step * 0.2) * 2
        
        # Outer pulse
        self.map_canvas.create_oval(
            x - pulse_size - 3, y - pulse_size - 3,
            x + pulse_size + 3, y + pulse_size + 3,
            fill='', outline='#FF5252', width=2,
            tags='marker'
        )
        
        # Inner marker
        self.map_canvas.create_oval(
            x - pulse_size, y - pulse_size,
            x + pulse_size, y + pulse_size,
            fill='#FF5252', outline='white', width=2,
            tags='marker'
        )
    
    def _draw_info_overlay(self, cx, cy, radius):
        """Draw city information overlay"""
        # Info box at bottom
        info_y = cy + radius + 30
        
        # City name
        self.map_canvas.create_text(
            cx, info_y,
            text=self.city_name,
            font=('Segoe UI', 16, 'bold'),
            fill='white',
            tags='info'
        )
        
        # Coordinates
        self.map_canvas.create_text(
            cx, info_y + 25,
            text=f"📍 {self.lat:.2f}°, {self.lon:.2f}°",
            font=('Segoe UI', 11),
            fill='#B0BEC5',
            tags='info'
        )
    
    def _start_animation(self):
        """Start the earth rotation animation"""
        if not self.is_animating:
            self.is_animating = True
            self._animate()
    
    def _animate(self):
        """Animate the earth rotation"""
        if not self.is_animating:
            return
        
        self.animation_step += 1
        self._draw_earth()
        
        # Continue animation
        self.after(50, self._animate)  # 20 FPS
    
    def _on_resize(self, event=None):
        """Handle canvas resize"""
        self._draw_earth()
    
    def update_location(self, city_name, lat, lon):
        """Update map to new location with ZOOM effect!"""
        print(f"🌍 Zooming to {city_name}...")
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        
        # Update title
        self.title_label.config(text=f"🌍 {city_name}")
        
        # Animate zoom in
        self._zoom_to_location()
    
    def _zoom_to_location(self):
        """Animated zoom effect"""
        target_zoom = 10
        
        def zoom_step():
            if self.zoom_level < target_zoom:
                self.zoom_level += 1
                self.zoom_label.config(text=f"🔍 Zooming... {self.zoom_level}/{target_zoom}")
                self._draw_earth()
                self.after(50, zoom_step)
            else:
                self.zoom_label.config(text=f"🔍 {self.city_name}")
                # Zoom back out after 2 seconds
                self.after(2000, self._zoom_out)
        
        zoom_step()
    
    def _zoom_out(self):
        """Zoom back out"""
        def zoom_step():
            if self.zoom_level > 0:
                self.zoom_level -= 1
                self.zoom_label.config(text=f"🔍 Global View")
                self._draw_earth()
                self.after(50, zoom_step)
        
        zoom_step()
    
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
        
        tk.Label(
            self,
            text="📍 Location Map",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
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