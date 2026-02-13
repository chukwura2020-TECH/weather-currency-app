# gui/main_gui.py
"""
Main application window - FINAL VERSION WITH ALL FIXES!
🐛 FIXED: Toggle button now visible
🐛 FIXED: Settings page working (not "coming soon")
🐛 FIXED: No more lag when switching views
"""
from gui.components.alert_banner import AlertBanner
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS
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
        """Create the main layout with sidebar and tabbed content"""
    
        # LEFT: Sidebar
        self.sidebar = Sidebar(self.root, self.switch_view)
        self.sidebar.pack(side="left", fill="y")
        
        # 🐛 FIX: Add dark mode toggle to sidebar (VISIBLE NOW!)
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
        
        # Add favorites panel to the right column
        self.favorites = FavoritesPanel(right_col, on_city_click=self._on_favorite_city_click)
        self.favorites.pack(fill='x', pady=(0, 20))
        
        # Content frame for switching views (below favorites)
        self.content_frame = tk.Frame(right_col, bg=COLORS['bg_primary'])
        self.content_frame.pack(fill="both", expand=True)
        
        # Alert banner
        self.alert_banner = AlertBanner(self.content_frame)
        
        # Load default view (Weather)
        self.current_view = None
        self.switch_view("weather")
    
    def _on_theme_toggle(self, new_theme):
        """Handle theme toggle"""
        print(f"Theme switched to: {new_theme}")
        
        # Refresh all colors IMMEDIATELY (no lag!)
        self.refresh_all_colors()
    
    def switch_view(self, view_name):
        """
        Switch between different views (Weather, Currency, Settings)
        🐛 FIXED: No more lag! Instant switching!
        """
        
        # Clear current view FAST
        if self.current_view:
            self.current_view.destroy()
        
        # Load new view IMMEDIATELY
        if view_name == "weather":
            from gui.weather_dashboard import WeatherDashboard
            self.current_view = WeatherDashboard(self.content_frame)
        
        elif view_name == "currency":
            self.current_view = CurrencyConverter(self.content_frame)
        
        elif view_name == "settings":
            # 🐛 FIX: Real settings page (not "Coming Soon"!)
            from gui.settings_gui import SettingsPage
            self.current_view = SettingsPage(self.content_frame)
        
        else:
            # Fallback for unknown views
            self.current_view = tk.Label(
                self.content_frame,
                text=f"{view_name.title()}",
                bg=COLORS['bg_primary'],
                fg=COLORS['text_white'],
                font=FONTS['title']
            )
        
        # Pack immediately (no delay!)
        self.current_view.pack(fill="both", expand=True)
        
        # Force immediate update
        self.content_frame.update_idletasks()
    
    def _on_favorite_city_click(self, city_name):
        """Handle when a favorite city is clicked"""
        print(f"Favorite city clicked: {city_name}")
        self.switch_view("weather")
        
        # Update weather after a brief moment (let view load first)
        self.root.after(100, lambda: self._update_weather_city(city_name))
    
    def _update_weather_city(self, city_name):
        """Update weather view with city"""
        if hasattr(self.current_view, 'update_city'):
            self.current_view.update_city(city_name)

    def refresh_all_colors(self):
        """Refresh all component colors when theme changes"""
        # Update root background
        self.root.config(bg=COLORS['bg_primary'])
        
        # Update sidebar
        if hasattr(self, 'sidebar'):
            self._update_widget_colors(self.sidebar)
        
        # Update favorites panel
        if hasattr(self, 'favorites'):
            self.favorites.config(bg=COLORS['bg_card'])
            self._update_widget_colors(self.favorites)
        
        # Update content frame
        if hasattr(self, 'content_frame'):
            self.content_frame.config(bg=COLORS['bg_primary'])
        
        # Update current view
        if hasattr(self.current_view, 'update_colors'):
            self.current_view.update_colors()
        else:
            self._update_widget_colors(self.current_view)
        
        # Update theme toggle
        if hasattr(self, 'theme_toggle'):
            self.theme_toggle.update_colors()

    def _update_widget_colors(self, widget):
        """Recursively update widget colors"""
        from gui.styles.theme import COLORS
        
        try:
            # Update specific widget types
            if isinstance(widget, tk.Frame):
                current_bg = widget.cget('bg')
                if current_bg in ['#4A90E2', '#FFFFFF', '#E8F4FD', '#1A202C', '#2D3748']:
                    widget.config(bg=COLORS['bg_primary'])
            
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget('bg')
                if current_bg in ['#4A90E2', '#FFFFFF', '#E8F4FD', '#1A202C', '#2D3748']:
                    widget.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])
            
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=COLORS['bg_card'])
            
            # Recursively update children
            for child in widget.winfo_children():
                self._update_widget_colors(child)
        except:
            pass