# gui/map_gui.py
"""
Map display component (placeholder for now).
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class MapPlaceholder(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white', height=200)
        
        self.pack_propagate(False)  # Maintain fixed height
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create map placeholder"""
        
        # Title
        tk.Label(
            self,
            text="Weather Map",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Map placeholder
        tk.Label(
            self,
            text="🗺️\n\nMap view coming soon...",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        ).pack(expand=True)