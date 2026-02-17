# gui/components/search_bar.py
"""
City search bar component.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class SearchBar(tk.Frame):
    """Search input for cities"""
    
    def __init__(self, parent, on_search_callback):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.on_search = on_search_callback
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create search input"""
        
        # Container
        search_frame = tk.Frame(self, bg='white')
        search_frame.pack(fill="x", padx=20, pady=20)
        
        # Search icon
        tk.Label(
            search_frame,
            text="🔍",
            bg='white',
            font=('Segoe UI', 16)
        ).pack(side="left", padx=(15, 10))
        
        # Search entry
        self.entry = tk.Entry(
            search_frame,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['subheading'],
            bd=0,
            relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.entry.insert(0, "Search for a city...")
        
        # Bind events
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
        # Search button
        search_btn = tk.Label(
            search_frame,
            text="→",
            bg='white',
            fg=COLORS['accent_blue'],
            font=('Segoe UI', 20),
            cursor='hand2',
            padx=15
        )
        search_btn.pack(side="right")
        search_btn.bind('<Button-1>', lambda e: self._on_enter())
    
    def _on_focus_in(self, event):
        """Clear placeholder on focus"""
        if self.entry.get() == "Search for a city...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS['text_dark'])
    
    def _on_focus_out(self, event):
        """Restore placeholder if empty"""
        if not self.entry.get():
            self.entry.insert(0, "Search for a city...")
            self.entry.config(fg=COLORS['text_muted'])
    
    def _on_enter(self, event=None):
        """Handle search on Enter key"""
        city = self.entry.get().strip()
        
        if city and city != "Search for a city...":
            self.on_search(city)
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])