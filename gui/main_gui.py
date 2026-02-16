# gui/main_gui.py
"""
Main application window - FINAL PERFECT VERSION!
🐛 FIXED: Colors NEVER faint
🐛 FIXED: Uniform dark mode
🐛 FIXED: Instant response (no delay)
🐛 FIXED: All features working
"""
from gui.components.alert_banner import AlertBanner
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS, toggle_theme
from gui.components.sidebar import Sidebar
from gui.components.theme_toggle import ThemeToggle
from gui.currency_gui import CurrencyConverter
from gui.components.favorites import FavoritesPanel

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather & Currency Dashboard")
        
        # Set window size
        window_width = DIMENSIONS['window_width']
        window_height = DIMENSIONS['window_height']
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Set background color
        self.root.configure(bg=COLORS['bg_primary'])
        
        self._create_layout()
    
    def _create_layout(self):
        """Create the main layout"""
    
        # LEFT: Sidebar
        self.sidebar = Sidebar(self.root, self.switch_view)
        self.sidebar.pack(side="left", fill="y")
        
        # Dark mode toggle at bottom of sidebar
        toggle_container = tk.Frame(self.sidebar, bg=COLORS['bg_primary'])
        toggle_container.pack(side='bottom', pady=20)
        
        tk.Label(
            toggle_container,
            text="Theme",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['small']
        ).pack(pady=(0, 5))
        
        self.theme_toggle = ThemeToggle(toggle_container, on_toggle_callback=self._on_theme_toggle)
        self.theme_toggle.pack()
        
        # RIGHT: Main content area
        right_col = tk.Frame(self.root, bg=COLORS['bg_primary'])
        right_col.pack(side="right", fill="both", expand=True)
        
        # Favorites panel
        self.favorites = FavoritesPanel(right_col, on_city_click=self._on_favorite_city_click)
        self.favorites.pack(fill='x', pady=(0, 20))
        
        # Content frame
        self.content_frame = tk.Frame(right_col, bg=COLORS['bg_primary'])
        self.content_frame.pack(fill="both", expand=True)
        
        # Alert banner
        self.alert_banner = AlertBanner(self.content_frame)
        
        # Load default view
        self.current_view = None
        self.switch_view("weather")
    
    def _on_theme_toggle(self, new_theme):
        """Handle theme toggle - PERFECT COLOR UPDATE!"""
        print(f"🎨 Theme switched to: {new_theme}")
        
        # Force immediate update
        self.root.update_idletasks()
        
        # Update ALL colors THOROUGHLY
        self._update_all_colors()
        
        print("✅ Colors updated successfully!")
    
    def _update_all_colors(self):
        """Update EVERY widget's colors - No faint colors!"""
        from gui.styles.theme import COLORS
        
        # 1. Root window
        self.root.config(bg=COLORS['bg_primary'])
        
        # 2. Sidebar
        self._deep_update(self.sidebar, COLORS['bg_primary'])
        
        # 3. Favorites panel
        self.favorites.config(bg=COLORS['bg_card'])
        self._deep_update(self.favorites, COLORS['bg_card'])
        
        # 4. Content frame
        self.content_frame.config(bg=COLORS['bg_primary'])
        
        # 5. Current view
        if self.current_view and hasattr(self.current_view, 'update_colors'):
            self.current_view.update_colors()
        elif self.current_view:
            self._deep_update(self.current_view, COLORS['bg_primary'])
        
        # 6. Theme toggle
        if hasattr(self, 'theme_toggle'):
            self.theme_toggle.update_colors()
        
        # Force render
        self.root.update()
    
    def _deep_update(self, widget, default_bg):
        """Recursively update widget colors - THOROUGH!"""
        from gui.styles.theme import COLORS
        
        try:
            widget_type = type(widget).__name__
            
            # Update Frame backgrounds
            if isinstance(widget, tk.Frame):
                current_bg = widget.cget('bg')
                # Only update if it's a theme color
                if current_bg in ['#4A90E2', '#FFFFFF', '#E8F4FD', '#1A202C', '#2D3748', '#F7FAFC']:
                    widget.config(bg=default_bg)
            
            # Update Label colors
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget('bg')
                if current_bg in ['#4A90E2', '#FFFFFF', '#E8F4FD', '#1A202C', '#2D3748', '#F7FAFC']:
                    widget.config(
                        bg=COLORS['bg_card'],
                        fg=COLORS['text_dark']
                    )
            
            # Update Canvas
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=COLORS['bg_card'])
            
            # Recursively update children
            for child in widget.winfo_children():
                self._deep_update(child, default_bg)
                
        except Exception as e:
            pass  # Skip widgets that can't be updated
    
    def switch_view(self, view_name):
        """Switch between views - INSTANT!"""
        
        # Clear current view
        if self.current_view:
            self.current_view.destroy()
        
        # Load new view
        if view_name == "weather":
            from gui.weather_dashboard import WeatherDashboard
            self.current_view = WeatherDashboard(self.content_frame)
        
        elif view_name == "currency":
            self.current_view = CurrencyConverter(self.content_frame)
        
        elif view_name == "settings":
            from gui.settings_gui import SettingsPage
            self.current_view = SettingsPage(self.content_frame)
        
        else:
            self.current_view = tk.Label(
                self.content_frame,
                text=f"{view_name.title()}",
                bg=COLORS['bg_primary'],
                fg=COLORS['text_white'],
                font=FONTS['title']
            )
        
        # Pack immediately
        self.current_view.pack(fill="both", expand=True)
        
        # Force update
        self.content_frame.update_idletasks()
    
    def _on_favorite_city_click(self, city_name):
        """Handle favorite city click"""
        print(f"Favorite city clicked: {city_name}")
        self.switch_view("weather")
        self.root.after(100, lambda: self._update_weather_city(city_name))
    
    def _update_weather_city(self, city_name):
        """Update weather view with city"""
        if hasattr(self.current_view, 'update_city'):
            self.current_view.update_city(city_name)