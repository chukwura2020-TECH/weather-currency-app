# gui/components/sidebar.py
"""
Navigation sidebar component.
🐛 FIXED: Weather icon now centered like the rest!
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS

class Sidebar(tk.Frame):
    """Left sidebar with navigation icons"""
    
    def __init__(self, parent, on_navigate):
        super().__init__(parent, bg=COLORS['bg_primary'], width=80)
        
        self.on_navigate = on_navigate
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create sidebar navigation buttons"""
        
        # Logo/Title area
        logo_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        logo_frame.pack(pady=30)
        
        tk.Label(
            logo_frame,
            text="⛅",
            bg=COLORS['bg_primary'],
            font=('Segoe UI', 32)
        ).pack()
        
        # Navigation buttons - ALL CENTERED!
        nav_items = [
            ("🌤️", "weather", "Weather"),
            ("💱", "currency", "Currency"),
            ("⚙️", "settings", "Settings"),
        ]
        
        for icon, view, tooltip in nav_items:
            self._create_nav_button(icon, view, tooltip)
    
    def _create_nav_button(self, icon, view, tooltip):
        """Create a single navigation button - PERFECTLY CENTERED!"""
        
        # Container frame to ensure centering
        btn_container = tk.Frame(self, bg=COLORS['bg_primary'])
        btn_container.pack(pady=10, fill='x')
        
        btn = tk.Label(
            btn_container,
            text=icon,
            bg=COLORS['bg_primary'],
            font=('Segoe UI', 28),
            cursor="hand2",
            padx=20,
            pady=15
        )
        btn.pack(anchor='center')  # CENTER IT!
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['accent_blue']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['bg_primary']))
        
        # Click handler
        btn.bind('<Button-1>', lambda e: self.on_navigate(view))
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])
        for child in self.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=COLORS['bg_primary'])
            elif isinstance(child, tk.Frame):
                child.config(bg=COLORS['bg_primary'])
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.config(bg=COLORS['bg_primary'])