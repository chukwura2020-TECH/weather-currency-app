# gui/map_gui.py
"""
Map display component with PROFESSIONAL, SUBTLE animation!
🐛 FIXED: Location marker STAYS IN PLACE (no left-right movement)
🐛 FIXED: Professional, elegant design (not childish)
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
import math

class WeatherMap(tk.Frame):
    """Professional weather map visualization"""
    
    def __init__(self, parent, city_name="London", lat=51.5074, lon=-0.1278):
        super().__init__(parent, bg='white', height=300)
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        self.animation_step = 0
        self.is_animating = False
        self.pulse_size = 0
        
        self.pack_propagate(False)
        
        self._create_widgets()
        self._start_animation()
    
    def _create_widgets(self):
        """Create professional map display"""
        
        # Header with gradient-like effect
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Title
        self.title_label = tk.Label(
            header,
            text=f"📍 {self.city_name}",
            bg='white',
            fg='#1A202C',
            font=('Segoe UI', 16, 'bold')
        )
        self.title_label.pack(side="left")
        
        # Status indicator
        self.status_label = tk.Label(
            header,
            text="● Live",
            bg='white',
            fg='#48BB78',
            font=('Segoe UI', 10)
        )
        self.status_label.pack(side="right")
        
        # Canvas for professional visualization
        self.map_canvas = tk.Canvas(
            self,
            bg='#F7FAFC',  # Light gray background
            highlightthickness=1,
            highlightbackground='#E2E8F0'
        )
        self.map_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Bind resize
        self.map_canvas.bind('<Configure>', self._on_resize)
        
        # Draw initial map
        self._draw_map()
    
    def _draw_map(self):
        """Draw professional map visualization"""
        self.map_canvas.delete('all')
        
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
        
        center_x = width // 2
        center_y = height // 2
        
        # Draw subtle grid pattern
        self._draw_grid(width, height)
        
        # Draw coordinate circles (latitude lines)
        self._draw_coordinate_circles(center_x, center_y, width, height)
        
        # Draw location marker (FIXED position - no movement!)
        self._draw_fixed_marker(center_x, center_y)
        
        # Draw info overlay
        self._draw_professional_info(center_x, center_y, height)
    
    def _draw_grid(self, width, height):
        """Draw subtle background grid"""
        # Vertical lines
        for x in range(0, width, 40):
            self.map_canvas.create_line(
                x, 0, x, height,
                fill='#E2E8F0', width=1
            )
        
        # Horizontal lines
        for y in range(0, height, 40):
            self.map_canvas.create_line(
                0, y, width, y,
                fill='#E2E8F0', width=1
            )
    
    def _draw_coordinate_circles(self, cx, cy, width, height):
        """Draw latitude/longitude circles"""
        max_radius = min(width, height) // 2 - 20
        
        # Draw 3 concentric circles
        for i in range(1, 4):
            radius = (max_radius // 3) * i
            
            # Circle
            self.map_canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline='#CBD5E0', width=2, dash=(5, 3)
            )
    
    def _draw_fixed_marker(self, cx, cy):
        """
        Draw location marker that STAYS IN PLACE
        Only subtle pulse animation - NO left-right movement!
        """
        # Pulse effect (gentle breathing)
        pulse = math.sin(self.animation_step * 0.1) * 2
        marker_size = 10 + pulse
        
        # Outer glow (subtle)
        glow_size = marker_size + 8
        self.map_canvas.create_oval(
            cx - glow_size, cy - glow_size,
            cx + glow_size, cy + glow_size,
            fill='#FED7D7', outline='',
            tags='marker'
        )
        
        # Middle ring
        ring_size = marker_size + 3
        self.map_canvas.create_oval(
            cx - ring_size, cy - ring_size,
            cx + ring_size, cy + ring_size,
            fill='#FC8181', outline='',
            tags='marker'
        )
        
        # Inner marker (solid)
        self.map_canvas.create_oval(
            cx - marker_size, cy - marker_size,
            cx + marker_size, cy + marker_size,
            fill='#E53E3E', outline='white', width=2,
            tags='marker'
        )
        
        # Center dot
        dot_size = 3
        self.map_canvas.create_oval(
            cx - dot_size, cy - dot_size,
            cx + dot_size, cy + dot_size,
            fill='white', outline='',
            tags='marker'
        )
    
    def _draw_professional_info(self, cx, cy, height):
        """Draw professional information overlay"""
        info_y = height - 40
        
        # City name with icon
        self.map_canvas.create_text(
            cx, info_y,
            text=f"📍 {self.city_name}",
            font=('Segoe UI', 14, 'bold'),
            fill='#1A202C'
        )
        
        # Coordinates (smaller, subtle)
        self.map_canvas.create_text(
            cx, info_y + 22,
            text=f"{self.lat:.4f}°N, {self.lon:.4f}°E",
            font=('Segoe UI', 9),
            fill='#718096'
        )
    
    def _start_animation(self):
        """Start subtle animation"""
        if not self.is_animating:
            self.is_animating = True
            self._animate()
    
    def _animate(self):
        """Gentle pulse animation - NO childish movements!"""
        if not self.is_animating:
            return
        
        self.animation_step += 1
        
        # Only redraw marker (not entire canvas) for performance
        self.map_canvas.delete('marker')
        
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        
        if width > 10 and height > 10:
            center_x = width // 2
            center_y = height // 2
            self._draw_fixed_marker(center_x, center_y)
        
        # Slower animation (30ms = ~33 FPS, smoother)
        self.after(30, self._animate)
    
    def _on_resize(self, event=None):
        """Handle canvas resize"""
        self._draw_map()
    
    def update_location(self, city_name, lat, lon):
        """Update map to new location"""
        print(f"📍 Updating to {city_name}")
        
        self.city_name = city_name
        self.lat = lat
        self.lon = lon
        
        # Update title
        self.title_label.config(text=f"📍 {city_name}")
        
        # Redraw map
        self._draw_map()
    
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
        
        map_frame = tk.Frame(self, bg='#F7FAFC', relief='solid', bd=1)
        map_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        tk.Label(
            map_frame,
            text="📍\n\nLocation tracking active\n💡 Professional maps in full version",
            bg='#F7FAFC',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        ).pack(expand=True)