# gui/components/sidebar.py
# gui/components/sidebar.py
"""
Sidebar navigation component with view switching.
"""
import tkinter as tk
from gui.styles.theme import COLORS, DIMENSIONS

class Sidebar(tk.Frame):
    def __init__(self, parent, switch_view_callback):
        super().__init__(
            parent, 
            bg=COLORS['bg_sidebar'], 
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
            bg=COLORS['bg_sidebar'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 32),
            pady=20
        )
        logo.pack(pady=(20, 40))
        
        # Navigation items with view names
        nav_items = [
            ("🏠", "weather", "Weather"),
            ("💱", "currency", "Currency"),
            ("⭐", "favorites", "Favorites"),
            ("⚙️", "settings", "Settings"),
        ]
        
        for icon, view_name, tooltip in nav_items:
            btn = tk.Label(
                self,
                text=icon,
                bg=COLORS['bg_sidebar'],
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
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['bg_sidebar']))