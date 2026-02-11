# gui/components/alert_banner.py
"""
Weather alert banner.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS

class AlertBanner(tk.Frame):
    """Display weather alerts"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='#FED7D7', height=60)
        self.pack_propagate(False)
        
        self._create_widgets()
        self.hide()
    
    def _create_widgets(self):
        """Create alert UI"""
        # Icon
        self.icon = tk.Label(
            self,
            text="⚠️",
            bg='#FED7D7',
            font=('Segoe UI', 24)
        )
        self.icon.pack(side='left', padx=15)
        
        # Alert text
        self.message = tk.Label(
            self,
            text="",
            bg='#FED7D7',
            fg='#742A2A',
            font=FONTS['body_bold'],
            wraplength=500,
            justify='left'
        )
        self.message.pack(side='left', fill='x', expand=True)
        
        # Close button
        close_btn = tk.Label(
            self,
            text="✕",
            bg='#FED7D7',
            fg='#742A2A',
            font=FONTS['heading'],
            cursor='hand2'
        )
        close_btn.pack(side='right', padx=15)
        close_btn.bind('<Button-1>', lambda e: self.hide())
    
    def show_alert(self, message, alert_type='warning'):
        """Show alert with message"""
        self.message.config(text=message)
        
        # Color based on type
        colors = {
            'warning': ('#FED7D7', '#742A2A'),  # Red
            'info': ('#BEE3F8', '#2C5282'),     # Blue
            'success': ('#C6F6D5', '#22543D'),  # Green
        }
        
        bg, fg = colors.get(alert_type, colors['warning'])
        
        self.config(bg=bg)
        self.icon.config(bg=bg)
        self.message.config(bg=bg, fg=fg)
        
        self.pack(fill='x', pady=(0, 10))
    
    def hide(self):
        """Hide alert"""
        self.pack_forget()