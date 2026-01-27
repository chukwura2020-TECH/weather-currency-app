# gui/components/summary_chart.py
"""
Summary chart component for hourly weather.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class SummaryChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create hourly summary chart"""
        
        # Title and tabs
        header = tk.Frame(self, bg='white')
        header.pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        tk.Label(
            header,
            text="Summary",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(side="left")
        
        # Right side tabs
        tabs = tk.Frame(header, bg='white')
        tabs.pack(side="right")
        
        for label in ["Summary", "Hourly", "Max Details"]:
            bg_color = COLORS['accent_blue'] if label == "Summary" else COLORS['accent_light']
            fg_color = 'white' if label == "Summary" else COLORS['text_dark']
            
            tk.Label(
                tabs,
                text=label,
                bg=bg_color,
                fg=fg_color,
                font=FONTS['small'],
                padx=10,
                pady=3
            ).pack(side="left", padx=2)
        
        # Chart placeholder (simplified)
        chart_frame = tk.Frame(self, bg='white', height=150)
        chart_frame.pack(fill="x", padx=DIMENSIONS['padding'], pady=(0, 15))
        chart_frame.pack_propagate(False)
        
        # Simple text-based chart placeholder
        tk.Label(
            chart_frame,
            text="📊 Hourly temperature chart\n(Visual chart coming soon)",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        ).pack(expand=True)