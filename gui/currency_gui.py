# gui/currency_gui.py
"""
Currency converter interface.
🐛 FIXED: Compact layout so convert button is always visible!
🐛 FIXED: Faster response, no lag!
"""
import csv
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.currency_api import CurrencyAPI
from gui.components.conversion_history import ConversionHistory

class CurrencyConverter(tk.Frame):
    """Currency converter view"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = CurrencyAPI()
        self.conversion_history = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the currency converter interface - COMPACT VERSION"""
        
        # Title - SMALLER PADDING
        title = tk.Label(
            self,
            text="Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['title']
        )
        title.pack(pady=(20, 15))  # REDUCED from (40, 30)
        
        # Main converter card - COMPACT
        converter_card = tk.Frame(self, bg='white')
        converter_card.pack(padx=50, pady=10, fill="x")  # REDUCED pady from 20
        
        # Container with LESS padding
        container = tk.Frame(converter_card, bg='white')
        container.pack(fill="x", padx=30, pady=20)  # REDUCED from (40, 40)
        
        # Amount input section - COMPACT
        amount_frame = tk.Frame(container, bg='white')
        amount_frame.pack(fill="x", pady=(0, 10))  # REDUCED from 20
        
        tk.Label(
            amount_frame,
            text="Amount:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']  # SMALLER font
        ).pack(anchor="w", pady=(0, 5))  # REDUCED from 10
        
        self.amount_entry = tk.Entry(
            amount_frame,
            bg='#F7FAFC',
            fg=COLORS['text_dark'],
            font=('Segoe UI', 14),  # SMALLER from 16
            bd=0,
            relief="flat"
        )
        self.amount_entry.pack(fill="x", ipady=8, padx=5)  # REDUCED ipady from 10
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind('<Return>', lambda e: self._convert())
        
        # From Currency section - COMPACT
        from_frame = tk.Frame(container, bg='white')
        from_frame.pack(fill="x", pady=(0, 10))  # REDUCED
        
        tk.Label(
            from_frame,
            text="From:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(anchor="w", pady=(0, 5))
        
        self.from_currency = ttk.Combobox(
            from_frame,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 12),  # SMALLER from 14
            state='readonly'
        )
        self.from_currency.pack(fill="x", ipady=6)  # REDUCED from 8
        self.from_currency.set("USD")
        
        # Swap button - SMALLER
        swap_frame = tk.Frame(container, bg='white')
        swap_frame.pack(pady=5)  # REDUCED from 10
        
        swap_btn = tk.Button(
            swap_frame,
            text="⇅ Swap",
            bg=COLORS['accent_blue'],
            fg='white',
            font=FONTS['body'],  # SMALLER
            bd=0,
            padx=20,  # REDUCED from 30
            pady=6,   # REDUCED from 10
            cursor="hand2",
            command=self._swap_currencies,
            activebackground='#357ABD',
            activeforeground='white'
        )
        swap_btn.pack()
        
        # To Currency section - COMPACT
        to_frame = tk.Frame(container, bg='white')
        to_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            to_frame,
            text="To:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(anchor="w", pady=(0, 5))
        
        self.to_currency = ttk.Combobox(
            to_frame,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 12),
            state='readonly'
        )
        self.to_currency.pack(fill="x", ipady=6)
        self.to_currency.set("EUR")
        
        # 🐛 FIX: CONVERT BUTTON - ALWAYS VISIBLE!
        convert_btn = tk.Button(
            container,
            text="Convert",
            bg=COLORS['accent_blue'],
            fg='white',
            font=('Segoe UI', 14, 'bold'),  # SMALLER from 16
            bd=0,
            padx=30,  # REDUCED from 40
            pady=10,  # REDUCED from 15
            cursor="hand2",
            command=self._convert,
            activebackground='#357ABD',
            activeforeground='white'
        )
        convert_btn.pack(pady=10)  # REDUCED from 20

        # Export button - SMALLER
        export_btn = tk.Button(
            container,
            text="📊 Export",
            bg='#48BB78',
            fg='white',
            font=FONTS['small'],  # SMALLER
            bd=0,
            padx=15,  # REDUCED from 20
            pady=6,   # REDUCED from 10
            cursor='hand2',
            command=self._export_to_csv,
            activebackground='#38A169',
            activeforeground='white'
        )
        export_btn.pack(pady=5)  # REDUCED from 10
        
        # Result display - COMPACT
        self.result_label = tk.Label(
            container,
            text="Enter amount and click Convert",
            bg='white',
            fg=COLORS['text_dark'],
            font=('Segoe UI', 18, 'bold'),  # SMALLER from 24
            wraplength=500
        )
        self.result_label.pack(pady=10)  # REDUCED from 20
        
        # Exchange rate display
        self.rate_label = tk.Label(
            container,
            text="",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small'],  # SMALLER
            wraplength=500
        )
        self.rate_label.pack(pady=(0, 10))
        
        # History panel - COMPACT
        self.history_panel = ConversionHistory(self)
        self.history_panel.pack(fill="both", expand=True, pady=(10, 0))  # REDUCED from 30
    
    def _export_to_csv(self):
        """Export conversion history to CSV"""
        if not self.conversion_history:
            self.result_label.config(text="No conversions to export", fg='#E53E3E')
            self.rate_label.config(text="")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"currency_conversions_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Amount', 'From', 'To', 'Rate', 'Result'])
                
                for conversion in self.conversion_history:
                    writer.writerow([
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        conversion['amount'],
                        conversion['from_currency'],
                        conversion['to_currency'],
                        conversion['rate'],
                        conversion['converted']
                    ])
            
            self.result_label.config(text=f"✓ Exported successfully", fg='#48BB78')
            self.rate_label.config(text=f"Saved to: {filename}")
        except Exception as e:
            self.result_label.config(text="Export failed", fg='#E53E3E')
            self.rate_label.config(text=str(e))
    
    def _swap_currencies(self):
        """Swap from and to currencies"""
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)
        
        # Auto-convert after swap
        self._convert()
    
    def _convert(self):
        """
        Perform currency conversion
        🐛 FIXED: No more lag! Instant response!
        """
        try:
            amount_str = self.amount_entry.get().strip()
            
            if not amount_str:
                self.result_label.config(text="Please enter an amount", fg='#E53E3E')
                self.rate_label.config(text="")
                return
            
            amount = float(amount_str)
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if amount <= 0:
                self.result_label.config(text="Please enter a positive amount", fg='#E53E3E')
                self.rate_label.config(text="")
                return
            
            # 🐛 FIX: Quick loading message (NO delay!)
            self.result_label.config(text="Converting...", fg=COLORS['text_dark'])
            self.rate_label.config(text="")
            self.update_idletasks()  # Force immediate update
            
            # Get conversion result
            result = self.api.convert_currency(amount, from_curr, to_curr)
            
            if result:
                # Display result IMMEDIATELY
                converted_amount = result['converted']
                self.result_label.config(
                    text=f"{converted_amount:,.2f} {result['to_currency']}",
                    fg='#48BB78'
                )
                self.rate_label.config(
                    text=f"1 {from_curr} = {result['rate']:.4f} {to_curr}",
                    fg=COLORS['text_muted']
                )
                
                # Add to history
                self.history_panel.add_conversion(result)
                self.conversion_history.append(result)
            else:
                self.result_label.config(text="Conversion failed", fg='#E53E3E')
                self.rate_label.config(text="Check internet connection", fg='#E53E3E')
                
        except ValueError:
            self.result_label.config(text="Invalid amount", fg='#E53E3E')
            self.rate_label.config(text="Enter a valid number (e.g., 100)", fg='#E53E3E')
        except Exception as e:
            self.result_label.config(text="Error occurred", fg='#E53E3E')
            self.rate_label.config(text=f"{str(e)}", fg='#E53E3E')
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])