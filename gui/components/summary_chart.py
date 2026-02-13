# gui/components/summary_chart.py
"""
Summary chart component for hourly weather.
NOW WITH REAL GRAPHS! 📊
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from datetime import datetime

class SummaryChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self.hourly_data = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create hourly summary chart"""
        
        # Title and tabs
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        tk.Label(
            header,
            text="Temperature Trend",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(side="left")
        
        # Right side tabs
        tabs = tk.Frame(header, bg='white')
        tabs.pack(side="right")
        
        self.tab_labels = {}
        for i, label in enumerate(["Hourly", "Daily", "Details"]):
            bg_color = COLORS['accent_blue'] if i == 0 else COLORS['accent_light']
            fg_color = 'white' if i == 0 else COLORS['text_dark']
            
            tab = tk.Label(
                tabs,
                text=label,
                bg=bg_color,
                fg=fg_color,
                font=FONTS['small'],
                padx=10,
                pady=3,
                cursor='hand2'
            )
            tab.pack(side="left", padx=2)
            self.tab_labels[label] = tab
        
        # Chart canvas
        self.chart_canvas = tk.Canvas(
            self,
            bg='white',
            height=180,
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="x", padx=DIMENSIONS['padding'], pady=(10, 15))
    
    def update_chart(self, forecast_data):
        """
        Update chart with forecast data.
        
        Args:
            forecast_data (dict): Forecast data from API
        """
        if not forecast_data or 'list' not in forecast_data:
            return
        
        # Clear canvas
        self.chart_canvas.delete('all')
        
        # Get hourly data (next 8 hours)
        hourly = forecast_data['list'][:8]
        
        if not hourly:
            return
        
        # Extract temperatures and times
        temps = [item['main']['temp'] for item in hourly]
        times = [datetime.fromtimestamp(item['dt']).strftime('%H:%M') for item in hourly]
        
        # Draw the chart
        self._draw_temperature_chart(temps, times)
    
    def _draw_temperature_chart(self, temps, times):
        """
        Draw temperature bar chart.
        
        Args:
            temps (list): List of temperatures
            times (list): List of time labels
        """
        if not temps:
            return
        
        canvas_width = self.chart_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 400
        
        canvas_height = 180
        padding = 40
        chart_height = canvas_height - padding - 30
        
        # Calculate positions
        num_bars = len(temps)
        bar_width = (canvas_width - 2 * padding) / num_bars * 0.7
        spacing = (canvas_width - 2 * padding) / num_bars
        
        # Find min/max for scaling
        min_temp = min(temps)
        max_temp = max(temps)
        temp_range = max_temp - min_temp
        if temp_range == 0:
            temp_range = 1
        
        # Draw grid lines
        for i in range(5):
            y = padding + (chart_height / 4) * i
            self.chart_canvas.create_line(
                padding, y, canvas_width - padding, y,
                fill='#E2E8F0', width=1
            )
        
        # Draw bars
        for i, (temp, time) in enumerate(zip(temps, times)):
            # Calculate bar height
            bar_height = ((temp - min_temp) / temp_range) * chart_height
            
            # Bar position
            x = padding + i * spacing + (spacing - bar_width) / 2
            y_bottom = padding + chart_height
            y_top = y_bottom - bar_height
            
            # Color gradient based on temperature
            if temp < 10:
                color = '#63B3ED'  # Cold - Blue
            elif temp < 20:
                color = '#48BB78'  # Mild - Green
            elif temp < 30:
                color = '#ED8936'  # Warm - Orange
            else:
                color = '#F56565'  # Hot - Red
            
            # Draw bar
            self.chart_canvas.create_rectangle(
                x, y_top, x + bar_width, y_bottom,
                fill=color, outline='', tags='bar'
            )
            
            # Draw temperature label on top of bar
            self.chart_canvas.create_text(
                x + bar_width / 2, y_top - 10,
                text=f"{temp:.0f}°",
                font=('Segoe UI', 10, 'bold'),
                fill=COLORS['text_dark']
            )
            
            # Draw time label below
            self.chart_canvas.create_text(
                x + bar_width / 2, y_bottom + 15,
                text=time,
                font=('Segoe UI', 9),
                fill=COLORS['text_muted']
            )
        
        # Draw min/max labels on the left
        self.chart_canvas.create_text(
            padding - 15, padding,
            text=f"{max_temp:.0f}°",
            font=('Segoe UI', 9),
            fill=COLORS['text_muted'],
            anchor='e'
        )
        
        self.chart_canvas.create_text(
            padding - 15, padding + chart_height,
            text=f"{min_temp:.0f}°",
            font=('Segoe UI', 9),
            fill=COLORS['text_muted'],
            anchor='e'
        )
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.chart_canvas.config(bg=COLORS['bg_card'])
        
        for label, widget in self.tab_labels.items():
            widget.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])