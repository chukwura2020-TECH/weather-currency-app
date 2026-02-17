# gui/components/conversion_history.py
"""
Conversion history display component.
"""
import tkinter as tk
from gui.styles.theme import COLORS, FONTS

class ConversionHistory(tk.Frame):
    """Display recent currency conversions"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create history display"""
        # Title
        title = tk.Label(
            self,
            text="Recent Conversions",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['heading']
        )
        title.pack(pady=(20, 10))
        
        # History container
        self.history_container = tk.Frame(self, bg=COLORS['bg_primary'])
        self.history_container.pack(fill="both", expand=True)
        
        # Initial message
        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.empty_label.pack(pady=20)
    
    def add_conversion(self, conversion_data):
        """
        Add a conversion to the history display.
        
        Args:
            conversion_data (dict): Contains 'amount', 'from_currency', 'to_currency', 'rate', 'converted'
        """
        # Remove empty message if it exists
        if self.empty_label.winfo_exists():
            self.empty_label.destroy()
        
        # Create conversion item
        item = tk.Frame(self.history_container, bg='white', relief='solid', bd=1)
        item.pack(fill="x", padx=20, pady=5)
        
        # Padding frame
        content = tk.Frame(item, bg='white')
        content.pack(fill="x", padx=15, pady=10)
        
        # Conversion text
        conversion_text = f"{conversion_data['amount']:.2f} {conversion_data['from_currency']} → {conversion_data['converted']:.2f} {conversion_data['to_currency']}"
        
        tk.Label(
            content,
            text=conversion_text,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(anchor="w")
        
        # Rate
        rate_text = f"Rate: 1 {conversion_data['from_currency']} = {conversion_data['rate']:.4f} {conversion_data['to_currency']}"
        
        tk.Label(
            content,
            text=rate_text,
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(anchor="w")
        
        # Keep only last 5 conversions visible
        children = self.history_container.winfo_children()
        if len(children) > 5:
            children[0].destroy()
    
    def clear_history(self):
        """Clear all history items"""
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        # Show empty message again
        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.empty_label.pack(pady=20)