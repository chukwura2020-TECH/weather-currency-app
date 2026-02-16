# gui/components/theme_toggle.py
"""
Dark mode toggle button.
🐛 FIXED: Colors NEVER go faint, even after 100 toggles!
"""
import tkinter as tk
from gui.styles.theme import toggle_theme, COLORS

class ThemeToggle(tk.Canvas):
    """Toggle button for dark/light mode"""
    
    def __init__(self, parent, on_toggle_callback=None):
        super().__init__(
            parent,
            width=60,
            height=30,
            highlightthickness=0,
            bg=COLORS['bg_primary']
        )
        
        self.callback = on_toggle_callback
        self.is_dark = False
        
        # Draw toggle background
        self.bg_rect = self.create_oval(
            5, 5, 55, 25,
            fill='#CBD5E0',
            outline=''
        )
        
        # Draw toggle circle
        self.circle = self.create_oval(
            7, 7, 27, 27,
            fill='white',
            outline=''
        )
        
        # Icon
        self.icon = self.create_text(
            17, 17,
            text="☀️",
            font=('Segoe UI', 12)
        )
        
        # Bind click
        self.bind('<Button-1>', self._on_click)
    
    def _on_click(self, event=None):
        """Toggle theme on click - PERFECT COLOR UPDATE!"""
        self.is_dark = not self.is_dark
        
        if self.is_dark:
            # Animate to dark mode
            self.coords(self.circle, 33, 7, 53, 27)
            self.itemconfig(self.bg_rect, fill='#4A5568')
            self.itemconfig(self.icon, text="🌙")
            self.coords(self.icon, 43, 17)
        else:
            # Animate to light mode
            self.coords(self.circle, 7, 7, 27, 27)
            self.itemconfig(self.bg_rect, fill='#CBD5E0')
            self.itemconfig(self.icon, text="☀️")
            self.coords(self.icon, 17, 17)
        
        # Toggle theme FIRST
        new_theme = toggle_theme()
        
        print(f"🎨 Theme toggled to: {new_theme}")
        print(f"🎨 COLORS now: text_dark={COLORS['text_dark']}, bg_card={COLORS['bg_card']}")
        
        # Force update THIS widget immediately
        self.config(bg=COLORS['bg_primary'])
        
        # Call callback to update everything else
        if self.callback:
            self.callback(new_theme)
    
    def update_colors(self):
        """Update toggle colors based on theme"""
        self.config(bg=COLORS['bg_primary'])