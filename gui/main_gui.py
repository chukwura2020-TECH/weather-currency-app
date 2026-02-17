# gui/main_gui.py
"""
Main application window - FINAL AGGRESSIVE VERSION!
🐛 FIXED: Colors NEVER EVER go faint - FORCED update system!
"""
from gui.components.alert_banner import AlertBanner
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, DIMENSIONS, FONTS, toggle_theme, is_dark_mode
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
        
        self.current_view_name = "weather"
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
        """
        Handle theme toggle - NUCLEAR OPTION!
        DESTROYS and RECREATES everything to force color update!
        """
        print(f"🎨 AGGRESSIVE theme switch to: {new_theme}")
        
        # Get current view name
        current_view = self.current_view_name
        
        # NUCLEAR OPTION: Destroy and recreate ENTIRE view!
        if self.current_view:
            self.current_view.destroy()
        
        # Force immediate recreation
        self.root.after(1, lambda: self._force_complete_refresh(current_view))
    
    def _force_complete_refresh(self, view_name):
        """COMPLETELY refresh the view with new colors"""
        from gui.styles.theme import COLORS
        
        print(f"🔥 FORCING complete refresh with new colors")
        print(f"   text_dark is now: {COLORS['text_dark']}")
        print(f"   bg_card is now: {COLORS['bg_card']}")
        
        # Update root
        self.root.config(bg=COLORS['bg_primary'])
        
        # Update sidebar
        self.sidebar.config(bg=COLORS['bg_primary'])
        self._nuclear_update(self.sidebar)
        
        # Update favorites
        self.favorites.config(bg=COLORS['bg_card'])
        self._nuclear_update(self.favorites)
        
        # Update content frame
        self.content_frame.config(bg=COLORS['bg_primary'])
        
        # Recreate current view with NEW colors
        self.switch_view(view_name)
        
        # Force render
        self.root.update()
        
        print(f"✅ Refresh complete!")
    
    def _nuclear_update(self, widget):
        """
        NUCLEAR color update - updates EVERYTHING recursively
        Uses CURRENT values from COLORS dict
        """
        from gui.styles.theme import COLORS
        
        try:
            # Update Frame
            if isinstance(widget, tk.Frame):
                widget.config(bg=COLORS['bg_primary'])
            
            # Update Label - FORCE new colors
            elif isinstance(widget, tk.Label):
                # Get current background
                try:
                    current_bg = widget.cget('bg')
                    # If it's ANY theme color, update it
                    if current_bg.startswith('#'):
                        widget.config(
                            bg=COLORS['bg_card'],
                            fg=COLORS['text_dark']
                        )
                except:
                    pass
            
            # Update Canvas
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=COLORS['bg_card'])
            
            # Recursively update ALL children
            for child in widget.winfo_children():
                self._nuclear_update(child)
                
        except Exception as e:
            pass
    
    def switch_view(self, view_name):
        """Switch between views"""
        
        # Save view name
        self.current_view_name = view_name
        
        # Clear current view
        if self.current_view:
            self.current_view.destroy()
        
        # Load new view with CURRENT colors
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