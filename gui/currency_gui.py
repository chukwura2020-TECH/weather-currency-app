<<<<<<< HEAD
import tkinter as tk


class CurrencyFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="💱 Currency Converter", font=("Arial", 18)).pack(pady=15)

        tk.Button(
            self,
            text="Back to Weather",
            command=lambda: controller.show_frame("WeatherFrame")
        ).pack()
=======
# gui/currency_gui.py
"""
Currency converter interface.
"""
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS, DIMENSIONS
from api.currency_api import CurrencyAPI

class CurrencyConverter(tk.Frame):
    """Currency converter view"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = CurrencyAPI()
        self.conversion_history = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the currency converter interface"""
        
        # Title
        title = tk.Label(
            self,
            text="Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['title']
        )
        title.pack(pady=(40, 30))
        
        # Main converter card
        converter_card = tk.Frame(self, bg='white')
        converter_card.pack(padx=50, pady=20, fill="both", expand=True)
        
        # Container with padding
        container = tk.Frame(converter_card, bg='white')
        container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Amount input section
        amount_frame = tk.Frame(container, bg='white')
        amount_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            amount_frame,
            text="Amount:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(anchor="w", pady=(0, 10))
        
        self.amount_entry = tk.Entry(
            amount_frame,
            bg='#F7FAFC',
            fg=COLORS['text_dark'],
            font=('Segoe UI', 16),
            bd=0,
            relief="flat"
        )
        self.amount_entry.pack(fill="x", ipady=10, padx=5)
        self.amount_entry.insert(0, "100")
        
        # From Currency section
        from_frame = tk.Frame(container, bg='white')
        from_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            from_frame,
            text="From:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(anchor="w", pady=(0, 10))
        
        self.from_currency = ttk.Combobox(
            from_frame,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 14),
            state='readonly'
        )
        self.from_currency.pack(fill="x", ipady=8)
        self.from_currency.set("USD")
        
        # Swap button
        swap_frame = tk.Frame(container, bg='white')
        swap_frame.pack(pady=10)
        
        swap_btn = tk.Button(
            swap_frame,
            text="⇅ Swap",
            bg=COLORS['accent_blue'],
            fg='white',
            font=FONTS['body_bold'],
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self._swap_currencies
        )
        swap_btn.pack()
        
        # To Currency section
        to_frame = tk.Frame(container, bg='white')
        to_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            to_frame,
            text="To:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(anchor="w", pady=(0, 10))
        
        self.to_currency = ttk.Combobox(
            to_frame,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 14),
            state='readonly'
        )
        self.to_currency.pack(fill="x", ipady=8)
        self.to_currency.set("EUR")
        
        # Convert button
        convert_btn = tk.Button(
            container,
            text="Convert",
            bg=COLORS['accent_blue'],
            fg='white',
            font=('Segoe UI', 16, 'bold'),
            bd=0,
            padx=40,
            pady=15,
            cursor="hand2",
            command=self._convert
        )
        convert_btn.pack(pady=20)
        
        # Result display
        self.result_label = tk.Label(
            container,
            text="",
            bg='white',
            fg=COLORS['text_dark'],
            font=('Segoe UI', 24, 'bold')
        )
        self.result_label.pack(pady=20)
        
        # Exchange rate display
        self.rate_label = tk.Label(
            container,
            text="",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['body']
        )
        self.rate_label.pack()
    
    def _swap_currencies(self):
        """Swap from and to currencies"""
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)
        
        # Auto-convert after swap
        self._convert()
    
    def _convert(self):
        """Perform currency conversion"""
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if amount <= 0:
                self.result_label.config(text="Please enter a positive amount")
                self.rate_label.config(text="")
                return
            
            # Show loading
            self.result_label.config(text="Converting...")
            self.rate_label.config(text="")
            self.update()
            
            # Get conversion result
            result = self.api.convert_currency(amount, from_curr, to_curr)
            
            if result:
                # Display result
                self.result_label.config(
                    text=f"{result['converted']} {result['to_currency']}"
                )
                self.rate_label.config(
                    text=f"1 {from_curr} = {result['rate']:.4f} {to_curr}"
                )
                
                # Add to history
                self.conversion_history.append(result)
            else:
                self.result_label.config(text="Conversion failed")
                self.rate_label.config(text="Please check your connection")
                
        except ValueError:
            self.result_label.config(text="Invalid amount")
            self.rate_label.config(text="Please enter a valid number")
>>>>>>> 7623fb2874d0efc944549ced80741849c835f8d1
