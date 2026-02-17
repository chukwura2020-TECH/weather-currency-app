# gui/components/sidebar.py
"""
Navigation sidebar component.
🐛 FIXED: Icons aligned WITHOUT pushing everything up!
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
        """Create sidebar navigation buttons - ALL ALIGNED with pack!"""
        
        # Logo/Title area
        logo_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        logo_frame.pack(pady=30)
        
        tk.Label(
            logo_frame,
            text="⛅",
            bg=COLORS['bg_primary'],
            font=('Segoe UI', 32)
        ).pack()
        
        # Navigation buttons container
        nav_container = tk.Frame(self, bg=COLORS['bg_primary'])
        nav_container.pack(pady=10)
        
        # Navigation buttons - ALL USE EXACT SAME LAYOUT!
        nav_items = [
            ("🌤️", "weather", "Weather"),
            ("💱", "currency", "Currency"),
            ("⚙️", "settings", "Settings"),
        ]
        
        for icon, view, tooltip in nav_items:
            self._create_nav_button(nav_container, icon, view, tooltip)
    
    def _create_nav_button(self, parent, icon, view, tooltip):
        """
        Create a single navigation button.
        ALL buttons use IDENTICAL pack parameters!
        """
        
        # Button frame - SAME for ALL
        btn_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        btn_frame.pack(pady=10)  # SAME spacing for ALL
        
        # Button label - SAME for ALL
        btn = tk.Label(
            btn_frame,
            text=icon,
            bg=COLORS['bg_primary'],
            font=('Segoe UI', 28),  # SAME font for ALL
            cursor="hand2",
            width=3  # SAME width for ALL - keeps them aligned!
        )
        btn.pack()  # Simple pack, no fancy parameters
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['accent_blue']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['bg_primary']))
        
        # Click handler
        btn.bind('<Button-1>', lambda e: self.on_navigate(view))
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])
        for child in self.winfo_children():
            self._update_child_colors(child)
    
    def _update_child_colors(self, widget):
        """Update colors recursively"""
        try:
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.config(bg=COLORS['bg_primary'])
            
            for child in widget.winfo_children():
                self._update_child_colors(child)
        except:
            pass