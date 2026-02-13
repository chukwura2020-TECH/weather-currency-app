# gui/components/favorites.py
"""
Favorites cities panel.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS
from utils.favorites import load_favorites, remove_favorite

class FavoritesPanel(tk.Frame):
    """Display favorite cities"""
    
    def __init__(self, parent, on_city_click=None):
        super().__init__(parent, bg=COLORS['bg_card'])
        
        self.on_city_click = on_city_click
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        """Create favorites list UI"""
        # Title
        title_frame = tk.Frame(self, bg=COLORS['bg_card'])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="⭐ Favorite Cities",
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(side='left')
        
        # Cities container
        self.cities_frame = tk.Frame(self, bg=COLORS['bg_card'])
        self.cities_frame.pack(fill='both', expand=True, padx=15)
    
    def refresh(self):
        """Refresh favorites list"""
        # Clear existing
        for widget in self.cities_frame.winfo_children():
            widget.destroy()
        
        # Load and display favorites
        favorites = load_favorites()
        
        if not favorites:
            tk.Label(
                self.cities_frame,
                text="No favorites yet",
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted'],
                font=FONTS['small']
            ).pack(pady=20)
        else:
            for city in favorites:
                self._create_city_item(city)
    
    def _create_city_item(self, city):
        """Create a single favorite city item"""
        item = tk.Frame(self.cities_frame, bg='white', height=50)
        item.pack(fill='x', pady=5)
        item.pack_propagate(False)
        
        # City name (clickable)
        name_label = tk.Label(
            item,
            text=city,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold'],
            cursor='hand2'
        )
        name_label.pack(side='left', padx=15)
        
        if self.on_city_click:
            name_label.bind('<Button-1>', lambda e: self.on_city_click(city))
        
        # Remove button
        remove_btn = tk.Label(
            item,
            text="✕",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            cursor='hand2'
        )
        remove_btn.pack(side='right', padx=15)
        remove_btn.bind('<Button-1>', lambda e: self._remove_city(city))
    
    def _remove_city(self, city):
        """Remove city from favorites"""
        remove_favorite(city)
        self.refresh()