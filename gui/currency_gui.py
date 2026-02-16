# gui/currency_gui.py
"""
Currency converter interface.
🐛 FIXED: Converter card now WIDE (700px) and PERFECTLY CENTERED!
🐛 FIXED: History also WIDE and CENTERED!
"""
import csv
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS
from api.currency_api import CurrencyAPI

class CurrencyConverter(tk.Frame):
    """Currency converter view - WIDE AND CENTERED VERSION"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = CurrencyAPI()
        self.conversion_history = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create WIDE and CENTERED currency converter"""
        
        # Title
        title = tk.Label(
            self,
            text="💱 Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 20, 'bold')
        )
        title.pack(pady=(10, 10))
        
        # Create scrollable canvas
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
        
        # ==== CONVERTER CARD - WIDE AND CENTERED! ====
        # Outer container to center everything
        converter_outer = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        converter_outer.pack(fill="both", expand=True, pady=5)
        
        # WIDE converter card (700px fixed width, centered)
        converter_card = tk.Frame(converter_outer, bg='#FFFFFF', width=700)
        converter_card.pack(anchor='center', padx=50)  # CENTERED!
        converter_card.pack_propagate(False)  # Fixed width
        
        # Inner container with padding
        container = tk.Frame(converter_card, bg='#FFFFFF')
        container.pack(fill="both", expand=True, padx=40, pady=25)
        
        # --- AMOUNT ---
        tk.Label(
            container,
            text="Amount:",
            bg='#FFFFFF',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor="w", pady=(0, 5))
        
        self.amount_entry = tk.Entry(
            container,
            bg='#EDF2F7',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 14),
            bd=1,
            relief="solid"
        )
        self.amount_entry.pack(fill="x", ipady=8)
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind('<Return>', lambda e: self._convert())
        
        # --- FROM CURRENCY ---
        tk.Label(
            container,
            text="From:",
            bg='#FFFFFF',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor="w", pady=(12, 5))
        
        self.from_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 12),
            state='readonly'
        )
        self.from_currency.pack(fill="x", ipady=6)
        self.from_currency.set("USD")
        
        # --- SWAP BUTTON ---
        swap_btn = tk.Button(
            container,
            text="⇅ Swap",
            bg='#4A90E2',
            fg='#FFFFFF',
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            padx=25,
            pady=8,
            cursor="hand2",
            command=self._swap_currencies,
            activebackground='#357ABD'
        )
        swap_btn.pack(pady=8)
        
        # --- TO CURRENCY ---
        tk.Label(
            container,
            text="To:",
            bg='#FFFFFF',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor="w", pady=(8, 5))
        
        self.to_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 12),
            state='readonly'
        )
        self.to_currency.pack(fill="x", ipady=6)
        self.to_currency.set("EUR")
        
        # --- CONVERT BUTTON (BIG!) ---
        convert_btn = tk.Button(
            container,
            text="Convert",
            bg='#48BB78',
            fg='#FFFFFF',
            font=('Segoe UI', 15, 'bold'),
            bd=0,
            padx=40,
            pady=12,
            cursor="hand2",
            command=self._convert,
            activebackground='#38A169'
        )
        convert_btn.pack(pady=15)
        
        # --- RESULT BOX (WIDE!) ---
        result_box = tk.Frame(container, bg='#EDF2F7', relief='solid', bd=2)
        result_box.pack(fill="x", pady=10)
        
        result_inner = tk.Frame(result_box, bg='#EDF2F7')
        result_inner.pack(padx=20, pady=15)
        
        self.result_label = tk.Label(
            result_inner,
            text="Enter amount and click Convert",
            bg='#EDF2F7',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 16, 'bold'),
            wraplength=600
        )
        self.result_label.pack()
        
        self.rate_label = tk.Label(
            result_inner,
            text="",
            bg='#EDF2F7',
            fg='#4A5568',  # Medium gray
            font=('Segoe UI', 11),
            wraplength=600
        )
        self.rate_label.pack(pady=(5, 0))
        
        # ==== HISTORY SECTION - WIDE AND CENTERED! ====
        history_outer = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        history_outer.pack(fill="both", expand=True, pady=(20, 10))
        
        # History header
        history_header_frame = tk.Frame(history_outer, bg=COLORS['bg_primary'], width=700)
        history_header_frame.pack(anchor='center', padx=50)
        history_header_frame.pack_propagate(False)
        
        tk.Label(
            history_header_frame,
            text="📜 Recent Conversions",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 15, 'bold')
        ).pack(pady=10)
        
        # History container - WIDE (700px)
        history_container_outer = tk.Frame(history_outer, bg=COLORS['bg_primary'], width=700)
        history_container_outer.pack(anchor='center', padx=50)
        history_container_outer.pack_propagate(False)
        
        self.history_container = tk.Frame(history_container_outer, bg=COLORS['bg_primary'])
        self.history_container.pack(fill="both", expand=True)
        
        # Initial empty message
        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet\nStart converting to see history!",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 12),
            justify="center"
        )
        self.empty_label.pack(pady=25)
    
    def _swap_currencies(self):
        """Swap currencies"""
        from_val = self.from_currency.get()
        to_val = self.to_currency.get()
        
        self.from_currency.set(to_val)
        self.to_currency.set(from_val)
        
        self._convert()
    
    def _convert(self):
        """Perform conversion"""
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
            
            self.result_label.config(text="⏳ Converting...", fg='#4A5568')
            self.rate_label.config(text="")
            self.update_idletasks()
            
            result = self.api.convert_currency(amount, from_curr, to_curr)
            
            if result:
                self.result_label.config(
                    text=f"✅ {result['converted']:,.2f} {result['to_currency']}",
                    fg='#48BB78'  # Green
                )
                self.rate_label.config(
                    text=f"Exchange Rate: 1 {from_curr} = {result['rate']:.4f} {to_curr}",
                    fg='#4A5568'
                )
                
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
        """Add to history - WIDE boxes!"""
        if self.empty_label.winfo_exists():
            self.empty_label.destroy()
        
        # History item - WIDE!
        item = tk.Frame(self.history_container, bg='#FFFFFF', relief='solid', bd=1)
        item.pack(fill="x", pady=5)
        
        content = tk.Frame(item, bg='#FFFFFF')
        content.pack(fill="x", padx=25, pady=15)
        
        # From amount
        tk.Label(
            content,
            text=f"{conversion_data['amount']:,.2f} {conversion_data['from_currency']}",
            bg='#FFFFFF',
            fg='#1A202C',  # DARK
            font=('Segoe UI', 13, 'bold')
        ).pack(anchor="w")
        
        # Arrow
        tk.Label(
            content,
            text="⬇",
            bg='#FFFFFF',
            fg='#4A5568',
            font=('Segoe UI', 14)
        ).pack(anchor="w", pady=3)
        
        # To amount
        tk.Label(
            content,
            text=f"{conversion_data['converted']:,.2f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#48BB78',  # Green
            font=('Segoe UI', 15, 'bold')
        ).pack(anchor="w")
        
        # Rate
        tk.Label(
            content,
            text=f"Rate: 1 {conversion_data['from_currency']} = {conversion_data['rate']:.4f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#718096',
            font=('Segoe UI', 10)
        ).pack(anchor="w", pady=(8, 0))
        
        # Keep only last 5
        children = self.history_container.winfo_children()
        if len(children) > 5:
            children[0].destroy()
    
    def update_colors(self):
        """Update colors"""
        self.config(bg=COLORS['bg_primary'])