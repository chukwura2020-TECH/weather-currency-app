# gui/currency_gui.py
"""
Currency converter interface.
🐛 FIXED: SINGLE WIDE converter box!
🐛 FIXED: Result inside the same box!
🐛 FIXED: Mousewheel scrolling works!
"""
import csv
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS
from api.currency_api import CurrencyAPI

class CurrencyConverter(tk.Frame):
    """Currency converter view - SINGLE WIDE BOX!"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.api = CurrencyAPI()
        self.conversion_history = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create SINGLE WIDE converter box with mousewheel scrolling"""
        
        # Title
        title = tk.Label(
            self,
            text="💱 Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 18, 'bold')
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
        
        # 🐛 FIX: MOUSEWHEEL SCROLLING!
        def _on_mousewheel(event):
            """Handle mousewheel scrolling"""
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_mousewheel_linux(event):
            """Handle mousewheel on Linux"""
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
        
        # Bind mousewheel events
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/Mac
        canvas.bind_all("<Button-4>", _on_mousewheel_linux)  # Linux scroll up
        canvas.bind_all("<Button-5>", _on_mousewheel_linux)  # Linux scroll down
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ==== SINGLE WIDE CONVERTER BOX ====
        converter_card = tk.Frame(scrollable_frame, bg='#FFFFFF', relief='solid', bd=1)
        converter_card.pack(fill="x", padx=80, pady=10)  # WIDER with 80px padding!
        
        container = tk.Frame(converter_card, bg='#FFFFFF')
        container.pack(fill="both", expand=True, padx=40, pady=25)  # Big internal padding
        
        # Amount
        tk.Label(
            container,
            text="Amount:",
            bg='#FFFFFF',
            fg='#1A202C',
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w", pady=(0, 3))
        
        self.amount_entry = tk.Entry(
            container,
            bg='#EDF2F7',
            fg='#1A202C',
            font=('Segoe UI', 13),
            bd=1,
            relief="solid"
        )
        self.amount_entry.pack(fill="x", ipady=6)
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind('<Return>', lambda e: self._convert())
        
        # From Currency
        tk.Label(
            container,
            text="From:",
            bg='#FFFFFF',
            fg='#1A202C',
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor="w", pady=(10, 3))
        
        self.from_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            font=('Segoe UI', 11),
            state='readonly'
        )
        self.from_currency.pack(fill="x", ipady=4)
        self.from_currency.set("USD")
        
        # Swap button
        swap_btn = tk.Button(
            container,
            text="⇅ Swap",
            bg='#4A90E2',
            fg='#FFFFFF',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=6,
            cursor="hand2",
            command=self._swap_currencies,
            activebackground='#357ABD'
        )
        swap_btn.pack(pady=8)
        
        # To Currency
        tk.Label(
            container,
            text="To:",
            bg='#FFFFFF',
            fg='#1A202C',
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
        
        # Convert button
        convert_btn = tk.Button(
            container,
            text="Convert",
            bg='#48BB78',
            fg='#FFFFFF',
            font=('Segoe UI', 13, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self._convert,
            activebackground='#38A169'
        )
        convert_btn.pack(pady=12)
        
        # Result box (inside same converter box!)
        result_box = tk.Frame(container, bg='#EDF2F7', relief='solid', bd=2)
        result_box.pack(fill="x", pady=(5, 0))
        
        result_inner = tk.Frame(result_box, bg='#EDF2F7')
        result_inner.pack(padx=20, pady=15)
        
        self.result_label = tk.Label(
            result_inner,
            text="Enter amount and click Convert",
            bg='#EDF2F7',
            fg='#1A202C',
            font=('Segoe UI', 16, 'bold'),
            wraplength=600
        )
        self.result_label.pack()
        
        self.rate_label = tk.Label(
            result_inner,
            text="",
            bg='#EDF2F7',
            fg='#4A5568',
            font=('Segoe UI', 11),
            wraplength=600
        )
        self.rate_label.pack(pady=(8, 0))
        
        # ==== HISTORY SECTION ====
        history_section = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        history_section.pack(fill="both", expand=True, padx=80, pady=(20, 20))
        
        # History header
        tk.Label(
            history_section,
            text="📜 Recent Conversions",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor="w", pady=(0, 10))
        
        # History container
        self.history_container = tk.Frame(history_section, bg=COLORS['bg_primary'])
        self.history_container.pack(fill="both", expand=True)
        
        # Initial empty message
        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet\nConvert some currency to see history here!",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 11),
            justify="center"
        )
        self.empty_label.pack(pady=20)
    
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
                    fg='#48BB78'
                )
                self.rate_label.config(
                    text=f"Exchange Rate: 1 {from_curr} = {result['rate']:.4f} {to_curr}",
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
        """Add to history - VISIBLE!"""
        # Remove empty message
        if self.empty_label and self.empty_label.winfo_exists():
            self.empty_label.destroy()
        
        # Create history item
        item = tk.Frame(self.history_container, bg='#FFFFFF', relief='solid', bd=1)
        item.pack(fill="x", pady=4)
        
        content = tk.Frame(item, bg='#FFFFFF')
        content.pack(fill="x", padx=20, pady=12)
        
        # From amount
        tk.Label(
            content,
            text=f"{conversion_data['amount']:,.2f} {conversion_data['from_currency']}",
            bg='#FFFFFF',
            fg='#1A202C',
            font=('Segoe UI', 12, 'bold')
        ).pack(anchor="w")
        
        # Arrow
        tk.Label(
            content,
            text="↓",
            bg='#FFFFFF',
            fg='#4A5568',
            font=('Segoe UI', 12)
        ).pack(anchor="w", pady=2)
        
        # To amount
        tk.Label(
            content,
            text=f"{conversion_data['converted']:,.2f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#48BB78',
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor="w")
        
        # Rate
        tk.Label(
            content,
            text=f"Rate: 1 {conversion_data['from_currency']} = {conversion_data['rate']:.4f} {conversion_data['to_currency']}",
            bg='#FFFFFF',
            fg='#718096',
            font=('Segoe UI', 9)
        ).pack(anchor="w", pady=(5, 0))
        
        # Keep only last 5
        children = self.history_container.winfo_children()
        if len(children) > 5:
            children[0].destroy()
    
    def update_colors(self):
        """Update colors"""
        self.config(bg=COLORS['bg_primary'])
