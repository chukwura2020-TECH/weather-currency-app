# gui/currency_gui.py
"""
Currency converter interface.
🐛 ULTRA COMPACT - Fits ANY screen size!
🐛 FIXED: Better colors (not faint)
🐛 FIXED: Result box and history ALWAYS visible
🐛 FIXED: No delay, instant response
"""
import csv
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS
from api.currency_api import CurrencyAPI

class CurrencyConverter(tk.Frame):
    """Currency converter view - ULTRA COMPACT VERSION"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = CurrencyAPI()
        self.conversion_history = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create ULTRA COMPACT currency converter"""
        
        # Title - TINY padding
        title = tk.Label(
            self,
            text="💱 Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 20, 'bold')  # Smaller from 32
        )
        title.pack(pady=(10, 10))  # TINY from (20, 15)
        
        # Create scrollable canvas for all content
        canvas = tk.Canvas(self, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main converter card - VERY COMPACT
        converter_card = tk.Frame(scrollable_frame, bg='#FFFFFF')  # Solid white (not faint!)
        converter_card.pack(padx=20, pady=5, fill="x")  # Tiny padding
        
        # Container - MINIMAL padding
        container = tk.Frame(converter_card, bg='#FFFFFF')
        container.pack(fill="x", padx=15, pady=15)  # Minimal
        
        # --- AMOUNT ---
        tk.Label(
            container,
            text="Amount:",
            bg='#FFFFFF',
            fg='#2D3748',  # DARK text (not faint!)
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w", pady=(0, 3))
        
        self.amount_entry = tk.Entry(
            container,
            bg='#EDF2F7',  # Light gray background
            fg='#1A202C',  # VERY DARK text
            font=('Segoe UI', 13),
            bd=1,
            relief="solid"
        )
        self.amount_entry.pack(fill="x", ipady=5)
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind('<Return>', lambda e: self._convert())
        
        # --- FROM CURRENCY ---
        tk.Label(
            container,
            text="From:",
            bg='#FFFFFF',
            fg='#2D3748',
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w", pady=(8, 3))
        
        self.from_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 11),
            state='readonly'
        )
        self.from_currency.pack(fill="x", ipady=4)
        self.from_currency.set("USD")
        
        # --- SWAP BUTTON ---
        swap_btn = tk.Button(
            container,
            text="⇅ Swap",
            bg='#4A90E2',  # BRIGHT blue
            fg='#FFFFFF',  # Pure white text
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._swap_currencies,
            activebackground='#357ABD'
        )
        swap_btn.pack(pady=5)
        
        # --- TO CURRENCY ---
        tk.Label(
            container,
            text="To:",
            bg='#FFFFFF',
            fg='#2D3748',
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w", pady=(5, 3))
        
        self.to_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 11),
            state='readonly'
        )
        self.to_currency.pack(fill="x", ipady=4)
        self.to_currency.set("EUR")
        
        # --- CONVERT BUTTON (BIG & VISIBLE!) ---
        convert_btn = tk.Button(
            container,
            text="Convert",
            bg='#48BB78',  # BRIGHT green
            fg='#FFFFFF',  # Pure white
            font=('Segoe UI', 13, 'bold'),
            bd=0,
            padx=25,
            pady=8,
            cursor="hand2",
            command=self._convert,
            activebackground='#38A169'
        )
        convert_btn.pack(pady=8)
        
        # --- RESULT BOX (ALWAYS VISIBLE!) ---
        result_box = tk.Frame(container, bg='#EDF2F7', relief='solid', bd=1)
        result_box.pack(fill="x", pady=5)
        
        result_inner = tk.Frame(result_box, bg='#EDF2F7')
        result_inner.pack(padx=10, pady=10)
        
        self.result_label = tk.Label(
            result_inner,
            text="Enter amount and click Convert",
            bg='#EDF2F7',
            fg='#2D3748',  # DARK text
            font=('Segoe UI', 14, 'bold'),
            wraplength=400
        )
        self.result_label.pack()
        
        self.rate_label = tk.Label(
            result_inner,
            text="",
            bg='#EDF2F7',
            fg='#4A5568',  # Medium dark gray
            font=('Segoe UI', 10),
            wraplength=400
        )
        self.rate_label.pack()
        
        # --- HISTORY SECTION (ALWAYS VISIBLE!) ---
        history_header = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        history_header.pack(fill="x", padx=20, pady=(10, 5))
        
        tk.Label(
            history_header,
            text="📜 Recent Conversions",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor="w")
        
        # History container
        self.history_container = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        self.history_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Initial empty message
        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet\nStart converting to see history!",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 11),
            justify="center"
        )
        self.empty_label.pack(pady=20)
    
    def _swap_currencies(self):
        """Swap from and to currencies - INSTANT!"""
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)
        
        self._convert()
    
    def _convert(self):
        """Perform currency conversion - INSTANT RESPONSE!"""
        try:
            amount_str = self.amount_entry.get().strip()
            
            if not amount_str:
                self.result_label.config(text="⚠️ Please enter an amount", fg='#E53E3E')
                self.rate_label.config(text="")
                return
            
            amount = float(amount_str)
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if amount <= 0:
                self.result_label.config(text="⚠️ Enter a positive amount", fg='#E53E3E')
                self.rate_label.config(text="")
                return
            
            # Show converting (INSTANT update!)
            self.result_label.config(text="⏳ Converting...", fg='#4A5568')
            self.rate_label.config(text="")
            self.update_idletasks()
            
            # Get conversion result
            result = self.api.convert_currency(amount, from_curr, to_curr)
            
            if result:
                # Show result in BIG BOLD text
                self.result_label.config(
                    text=f"✅ {result['converted']:,.2f} {result['to_currency']}",
                    fg='#48BB78'  # BRIGHT green
                )
                self.rate_label.config(
                    text=f"Rate: 1 {from_curr} = {result['rate']:.4f} {to_curr}",
                    fg='#4A5568'
                )
                
                # Add to history
                self._add_to_history(result)
                self.conversion_history.append(result)
            else:
                self.result_label.config(text="❌ Conversion failed", fg='#E53E3E')
                self.rate_label.config(text="Check internet connection", fg='#E53E3E')
                
        except ValueError:
            self.result_label.config(text="❌ Invalid amount", fg='#E53E3E')
            self.rate_label.config(text="Enter a valid number", fg='#E53E3E')
        except Exception as e:
            self.result_label.config(text="❌ Error occurred", fg='#E53E3E')
            self.rate_label.config(text=str(e), fg='#E53E3E')
    
    def _add_to_history(self, conversion_data):
        """Add conversion to history display"""
        # Remove empty message
        if self.empty_label.winfo_exists():
            self.empty_label.destroy()
        
        # Create history item with SOLID colors
        item = tk.Frame(self.history_container, bg='#FFFFFF', relief='solid', bd=1)
        item.pack(fill="x", pady=3)
        
        content = tk.Frame(item, bg='#FFFFFF')
        content.pack(fill="x", padx=10, pady=8)
        
        # From
        tk.Label(
            content,
            text=f"{conversion_data['amount']} {conversion_data['from_currency']}",
            bg='#FFFFFF',
            fg='#2D3748',  # DARK text
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w")
        
        # Arrow
        tk.Label(
            content,
            text="↓",
            bg='#FFFFFF',
            fg='#4A5568',
            font=('Segoe UI', 10)
        ).pack(anchor="w")
        
        # To
        tk.Label(
            content,
            text=f"{conversion_data['converted']:,.2f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#48BB78',  # BRIGHT green
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor="w")
        
        # Rate
        tk.Label(
            content,
            text=f"Rate: 1 {conversion_data['from_currency']} = {conversion_data['rate']:.4f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#718096',
            font=('Segoe UI', 9)
        ).pack(anchor="w", pady=(3, 0))
        
        # Keep only last 5
        children = self.history_container.winfo_children()
        if len(children) > 5:
            children[0].destroy()
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])
        # Note: This version uses SOLID colors that work in both themes