# gui/components/alert_banner.py
"""
Weather alert banner.
NOW WITH REAL ALERTS FROM API! ⚠️
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS

class AlertBanner(tk.Frame):
    """Display weather alerts from API"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='#FED7D7', height=60)
        self.pack_propagate(False)
        
        self._create_widgets()
        self.hide()
    
    def _create_widgets(self):
        """Create alert UI"""
        # Icon
        self.icon = tk.Label(
            self,
            text="⚠️",
            bg='#FED7D7',
            font=('Segoe UI', 24)
        )
        self.icon.pack(side='left', padx=15)
        
        # Alert text
        self.message = tk.Label(
            self,
            text="",
            bg='#FED7D7',
            fg='#742A2A',
            font=FONTS['body_bold'],
            wraplength=500,
            justify='left'
        )
        self.message.pack(side='left', fill='x', expand=True)
        
        # Close button
        close_btn = tk.Label(
            self,
            text="✕",
            bg='#FED7D7',
            fg='#742A2A',
            font=FONTS['heading'],
            cursor='hand2'
        )
        close_btn.pack(side='right', padx=15)
        close_btn.bind('<Button-1>', lambda e: self.hide())
    
    def show_alert(self, message, alert_type='warning'):
        """Show alert with message"""
        self.message.config(text=message)
        
        # Color based on type
        colors = {
            'warning': ('#FED7D7', '#742A2A'),  # Red
            'info': ('#BEE3F8', '#2C5282'),     # Blue
            'success': ('#C6F6D5', '#22543D'),  # Green
        }
        
        bg, fg = colors.get(alert_type, colors['warning'])
        
        self.config(bg=bg)
        self.icon.config(bg=bg)
        self.message.config(bg=bg, fg=fg)
        
        # Update close button
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget('text') == '✕':
                widget.config(bg=bg, fg=fg)
        
        self.pack(fill='x', pady=(0, 10))
    
    def hide(self):
        """Hide alert"""
        self.pack_forget()
    
    def check_weather_alerts(self, weather_data):
        """
        Check weather data for alert conditions.
        
        Args:
            weather_data (dict): Weather data from API
        """
        if not weather_data:
            return
        
        alerts = []
        
        # Check for extreme weather conditions
        try:
            # Heavy rain
            if 'rain' in weather_data and weather_data['rain'].get('1h', 0) > 10:
                alerts.append("Heavy rain expected!")
            
            # Strong winds
            wind_speed = weather_data.get('wind', {}).get('speed', 0)
            if wind_speed > 15:  # m/s (about 33 mph)
                alerts.append(f"Strong winds: {wind_speed:.1f} m/s!")
            
            # Extreme temperatures
            temp = weather_data.get('main', {}).get('temp', 0)
            if temp > 35:  # Celsius
                alerts.append(f"Extreme heat: {temp:.0f}°C!")
            elif temp < -10:
                alerts.append(f"Extreme cold: {temp:.0f}°C!")
            
            # Storm conditions
            weather_main = weather_data.get('weather', [{}])[0].get('main', '')
            if weather_main == 'Thunderstorm':
                alerts.append("⚡ Thunderstorm Alert!")
            elif weather_main == 'Snow':
                alerts.append("❄️ Snow Alert!")
            
            # Poor visibility
            visibility = weather_data.get('visibility', 10000)
            if visibility < 1000:  # Less than 1km
                alerts.append("⚠️ Poor visibility!")
            
            # Show alert if any conditions met
            if alerts:
                self.show_alert(" • ".join(alerts), 'warning')
            else:
                self.hide()
                
        except Exception as e:
            print(f"Error checking alerts: {e}")
    
    def update_colors(self):
        """Update colors when theme changes"""
        # Alert banner keeps its color regardless of theme
        pass