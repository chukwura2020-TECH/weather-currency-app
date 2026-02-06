# gui/components/conversion_history.py
"""
Conversion history display component.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS

class ConversionHistory(tk.Frame):
    """Display recent currency conversions"""
    
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create history display"""
        
        # Title
        tk.Label(
            self,
            text="Recent Conversions",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading'],
            anchor="w"
        ).pack(fill="x", padx=DIMENSIONS['padding'], pady=(15, 10))
        
        # Scrollable history container
        self.canvas = tk.Canvas(self, bg='white', highlightthickness=0, height=300)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.history_frame = tk.Frame(self.canvas, bg='white')
        
        self.history_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.history_frame, anchor="nw", width=380)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(15, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 15))
        
        # Empty state
        self.empty_label = tk.Label(
            self.history_frame,
            text="No conversions yet.\nStart converting to see history!",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        )
        self.empty_label.pack(pady=40)
    
    def add_conversion(self, conversion_data):
        """
        Add a conversion to history.
        
        Args:
            conversion_data (dict): Contains amount, from_currency, to_currency, rate, converted
        """
        # Remove empty state
        if self.empty_label.winfo_exists():
            self.empty_label.destroy()
        
        # Create history item
        item = tk.Frame(self.history_frame, bg='#F7FAFC')
        item.pack(fill="x", padx=10, pady=5)
        
        # Container with padding
        content = tk.Frame(item, bg='#F7FAFC')
        content.pack(fill="x", padx=15, pady=10)
        
        # From amount and currency
        tk.Label(
            content,
            text=f"{conversion_data['amount']} {conversion_data['from_currency']}",
            bg='#F7FAFC',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(anchor="w")
        
        # Arrow
        tk.Label(
            content,
            text="↓",
            bg='#F7FAFC',
            fg=COLORS['text_muted'],
            font=('Segoe UI', 12)
        ).pack(anchor="w")
        
        # To amount and currency
        tk.Label(
            content,
            text=f"{conversion_data['converted']} {conversion_data['to_currency']}",
            bg='#F7FAFC',
            fg=COLORS['accent_blue'],
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor="w")
        
        # Exchange rate
        tk.Label(
            content,
            text=f"Rate: 1 {conversion_data['from_currency']} = {conversion_data['rate']:.4f} {conversion_data['to_currency']}",
            bg='#F7FAFC',
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(anchor="w", pady=(5, 0))
    
    def clear_history(self):
        """Clear all history items"""
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Show empty state again
        self.empty_label = tk.Label(
            self.history_frame,
            text="No conversions yet.\nStart converting to see history!",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body'],
            justify="center"
        )
        self.empty_label.pack(pady=40)