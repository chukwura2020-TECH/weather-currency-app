# gui/components/search_bar.py
"""
Search bar component for location search.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS

class SearchBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create search input with icon"""
        
        # Container with white background (simulates rounded search box)
        search_container = tk.Frame(self, bg='white', height=45)
        search_container.pack(fill="x", padx=20, pady=20)
        search_container.pack_propagate(False)
        
        # Search icon
        icon = tk.Label(
            search_container,
            text="🔍",
            bg='white',
            font=('Segoe UI', 16)
        )
        icon.pack(side="left", padx=(15, 5))
        
        # Search entry field
        self.entry = tk.Entry(
            search_container,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body'],
            bd=0,
            relief="flat"
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=5)
        self.entry.insert(0, "Search for location")
        
        # Placeholder behavior
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)
    
    def _clear_placeholder(self, event):
        if self.entry.get() == "Search for location":
            self.entry.delete(0, tk.END)
    
    def _restore_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Search for location")