# gui/components/sidebar.py
"""
Sidebar navigation component.
"""
import tkinter as tk
from gui.styles.theme import COLORS, DIMENSIONS

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent, 
            bg=COLORS['bg_sidebar'], 
            width=DIMENSIONS['sidebar_width']
        )
        
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
        
        # Navigation buttons (using emojis as icons)
        nav_items = [
            "🏠",  # Home
            "🔄",  # Refresh
            "⭐",  # Favorites
            "⚙️",  # Settings
        ]
        
        for icon in nav_items:
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
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS['bg_secondary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS['bg_sidebar']))