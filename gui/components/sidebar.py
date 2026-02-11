# gui/components/sidebar.py
# gui/components/sidebar.py
"""
Sidebar navigation component with view switching.
"""
from gui.components.theme_toggle import ThemeToggle
import tkinter as tk
from gui.styles.theme import COLORS, DIMENSIONS

class Sidebar(tk.Frame):
    def __init__(self, parent, switch_view_callback):
        super().__init__(
            parent, 
            bg=COLORS['sidebar_bg'], 
            width=DIMENSIONS['sidebar_width']
        )
        
        self.switch_view = switch_view_callback
        
        # Prevent the frame from shrinking
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create navigation buttons"""
        
        # App logo/icon at the top
        logo = tk.Label(
            self,
            text="🌤️",
            bg=COLORS['sidebar_bg'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 32),
            pady=20
        )
        logo.pack(pady=(20, 40))
        
        # Navigation items with view names
        nav_items = [
            ("⛅", "weather", "Weather"),
            ("💱", "currency", "Currency"),
            ("⭐", "favorites", "Favorites"),
            ("⚙️", "settings", "Settings"),
        ]
        
        for icon, view_name, tooltip in nav_items:
            btn = tk.Label(
                self,
                text=icon,
                bg=COLORS['sidebar_bg'],
                fg=COLORS['text_white'],
                font=('Segoe UI', 24),
                cursor="hand2",
                pady=15
            )
            btn.pack(pady=10)
            
            # Click handler
            btn.bind("<Button-1>", lambda e, v=view_name: self.switch_view(v))
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['bg_secondary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['sidebar_bg']))

            # Dark mode toggle
        tk.Frame(self, bg=COLORS['sidebar_bg'], height=20).pack()
        self.theme_toggle = ThemeToggle(self, on_toggle_callback=self._on_theme_toggle)
        self.theme_toggle.pack(pady=10)

    def _on_theme_toggle(self, new_theme):
        """Handle theme toggle"""
        print(f"Theme switched to: {new_theme}")
        # Tell main window to refresh
        if hasattr(self.master, 'refresh_all_colors'):
         self.master.refresh_all_colors()