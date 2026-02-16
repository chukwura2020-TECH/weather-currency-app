# gui/components/summary_chart.py
"""
Summary chart component for hourly weather.
🐛 FIXED: ALL tabs now work! (Hourly, Daily, Details)
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from datetime import datetime

class SummaryChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self.hourly_data = []
        self.current_tab = "Hourly"
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
        
        # Right side tabs - ALL FUNCTIONAL!
        tabs = tk.Frame(header, bg='white')
        tabs.pack(side="right")
        
        self.tab_buttons = {}
        for label in ["Hourly", "Daily", "Details"]:
            bg_color = COLORS['accent_blue'] if label == "Hourly" else COLORS['accent_light']
            fg_color = 'white' if label == "Hourly" else COLORS['text_dark']
            
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
            tab.bind('<Button-1>', lambda e, l=label: self._switch_tab(l))
            self.tab_buttons[label] = tab
        
        # Chart canvas
        self.chart_canvas = tk.Canvas(
            self,
            bg='white',
            height=180,
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="x", padx=DIMENSIONS['padding'], pady=(10, 15))
    
    def _switch_tab(self, tab_name):
        """Switch between tabs - ALL WORK NOW!"""
        print(f"📊 Switching to {tab_name} tab")
        
        self.current_tab = tab_name
        
        # Update tab colors
        for name, button in self.tab_buttons.items():
            if name == tab_name:
                button.config(bg=COLORS['accent_blue'], fg='white')
            else:
                button.config(bg=COLORS['accent_light'], fg=COLORS['text_dark'])
        
        # Redraw chart with appropriate data
        if tab_name == "Hourly":
            self._show_hourly_view()
        elif tab_name == "Daily":
            self._show_daily_view()
        elif tab_name == "Details":
            self._show_details_view()
    
    def _show_hourly_view(self):
        """Show hourly temperature view"""
        self.chart_canvas.delete('all')
        
        if self.hourly_data:
            temps = [item['main']['temp'] for item in self.hourly_data[:8]]
            times = [datetime.fromtimestamp(item['dt']).strftime('%H:%M') for item in self.hourly_data[:8]]
            self._draw_temperature_chart(temps, times, "Hourly")
        else:
            self._show_placeholder("Hourly temperature data\nwill appear here")
    
    def _show_daily_view(self):
        """Show daily temperature view"""
        self.chart_canvas.delete('all')
        
        if self.hourly_data:
            # Get daily averages (every 8th item = 1 day)
            daily_temps = []
            daily_labels = []
            
            for i in range(0, min(len(self.hourly_data), 40), 8):
                day_items = self.hourly_data[i:i+8]
                avg_temp = sum(item['main']['temp'] for item in day_items) / len(day_items)
                daily_temps.append(avg_temp)
                
                date = datetime.fromtimestamp(day_items[0]['dt'])
                daily_labels.append(date.strftime('%a'))
            
            self._draw_temperature_chart(daily_temps, daily_labels, "Daily")
        else:
            self._show_placeholder("Daily temperature data\nwill appear here")
    
    def _show_details_view(self):
        """Show detailed weather info"""
        self.chart_canvas.delete('all')
        
        if self.hourly_data and len(self.hourly_data) > 0:
            item = self.hourly_data[0]
            
            # Draw details
            y = 30
            details = [
                f"🌡️ Temperature: {item['main']['temp']:.1f}°C",
                f"🌡️ Feels Like: {item['main']['feels_like']:.1f}°C",
                f"💧 Humidity: {item['main']['humidity']}%",
                f"💨 Wind: {item.get('wind', {}).get('speed', 0):.1f} m/s",
                f"☁️ Clouds: {item.get('clouds', {}).get('all', 0)}%",
                f"⏲️ Pressure: {item['main']['pressure']} hPa",
            ]
            
            for detail in details:
                self.chart_canvas.create_text(
                    200, y,
                    text=detail,
                    font=('Segoe UI', 12, 'bold'),
                    fill='#2D3748',
                    anchor='w'
                )
                y += 25
        else:
            self._show_placeholder("Detailed weather information\nwill appear here")
    
    def _show_placeholder(self, text):
        """Show placeholder text"""
        self.chart_canvas.create_text(
            200, 90,
            text=text,
            font=('Segoe UI', 11),
            fill=COLORS['text_muted'],
            justify='center'
        )
    
    def update_chart(self, forecast_data):
        """Update chart with forecast data"""
        if not forecast_data or 'list' not in forecast_data:
            return
        
        # Store hourly data
        self.hourly_data = forecast_data['list']
        
        # Redraw current view
        if self.current_tab == "Hourly":
            self._show_hourly_view()
        elif self.current_tab == "Daily":
            self._show_daily_view()
        elif self.current_tab == "Details":
            self._show_details_view()
    
    def _draw_temperature_chart(self, temps, times, chart_type="Hourly"):
        """Draw temperature bar chart"""
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
            bar_height = ((temp - min_temp) / temp_range) * chart_height
            
            x = padding + i * spacing + (spacing - bar_width) / 2
            y_bottom = padding + chart_height
            y_top = y_bottom - bar_height
            
            # Color based on temp
            if temp < 10:
                color = '#63B3ED'
            elif temp < 20:
                color = '#48BB78'
            elif temp < 30:
                color = '#ED8936'
            else:
                color = '#F56565'
            
            # Draw bar
            self.chart_canvas.create_rectangle(
                x, y_top, x + bar_width, y_bottom,
                fill=color, outline=''
            )
            
            # Temp label
            self.chart_canvas.create_text(
                x + bar_width / 2, y_top - 10,
                text=f"{temp:.0f}°",
                font=('Segoe UI', 10, 'bold'),
                fill='#2D3748'
            )
            
            # Time label
            self.chart_canvas.create_text(
                x + bar_width / 2, y_bottom + 15,
                text=time,
                font=('Segoe UI', 9),
                fill='#718096'
            )
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.chart_canvas.config(bg=COLORS['bg_card'])