# gui/currency_gui.py
"""
Currency converter interface.
✅ FIXED layout collapse
✅ Centered cards
✅ Wider responsive design
"""

import tkinter as tk
from tkinter import ttk
from gui.styles.theme import COLORS, FONTS
from api.currency_api import CurrencyAPI


class CurrencyConverter(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])

        self.api = CurrencyAPI()
        self.conversion_history = []

        self._create_widgets()

    def _create_widgets(self):

        # ---------- TITLE ----------
        title = tk.Label(
            self,
            text="💱 Currency Converter",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 20, 'bold')
        )
        title.pack(pady=(15, 15))

        # ---------- SCROLL CANVAS ----------
        canvas = tk.Canvas(self, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_primary'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------- CONVERTER CARD ----------
        converter_card = tk.Frame(
            scrollable_frame,
            bg='white'
        )

        converter_card.pack(
            pady=10,
            ipadx=20,
            ipady=10,
            padx=120,   # Controls horizontal centering width
            fill="x"
        )

        container = tk.Frame(converter_card, bg='white')
        container.pack(fill="x", padx=20, pady=20)

        # Amount
        tk.Label(container, text="Amount:", bg='white', fg='#2D3748',
                 font=('Segoe UI', 11, 'bold')).pack(anchor="w")

        self.amount_entry = tk.Entry(container, bg='#EDF2F7', font=('Segoe UI', 13))
        self.amount_entry.pack(fill="x", ipady=6, pady=(0, 8))
        self.amount_entry.insert(0, "100")

        # From Currency
        tk.Label(container, text="From:", bg='white', fg='#2D3748',
                 font=('Segoe UI', 11, 'bold')).pack(anchor="w")

        self.from_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            state="readonly"
        )
        self.from_currency.pack(fill="x", pady=(0, 8))
        self.from_currency.set("USD")

        # To Currency
        tk.Label(container, text="To:", bg='white', fg='#2D3748',
                 font=('Segoe UI', 11, 'bold')).pack(anchor="w")

        self.to_currency = ttk.Combobox(
            container,
            values=self.api.get_supported_currencies(),
            state="readonly"
        )
        self.to_currency.pack(fill="x", pady=(0, 12))
        self.to_currency.set("EUR")

        # Convert Button
        tk.Button(
            container,
            text="Convert",
            bg='#48BB78',
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            command=self._convert
        ).pack(pady=5)

        # Result Box
        result_box = tk.Frame(container, bg='#EDF2F7', bd=1, relief="solid")
        result_box.pack(fill="x", pady=10)

        self.result_label = tk.Label(
            result_box,
            text="Enter amount and click Convert",
            bg='#EDF2F7',
            font=('Segoe UI', 14, 'bold')
        )
        self.result_label.pack(padx=10, pady=10)

        # ---------- HISTORY ----------
        history_title = tk.Label(
            scrollable_frame,
            text="📜 Recent Conversions",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=('Segoe UI', 14, 'bold')
        )
        history_title.pack(pady=(20, 10))

        self.history_container = tk.Frame(scrollable_frame, bg=COLORS['bg_primary'])
        self.history_container.pack(
            padx=120,
            fill="x"
        )

        self.empty_label = tk.Label(
            self.history_container,
            text="No conversions yet",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white']
        )
        self.empty_label.pack(pady=20)

    # ---------- LOGIC ----------
    def _convert(self):

        try:
            amount = float(self.amount_entry.get())
            result = self.api.convert_currency(
                amount,
                self.from_currency.get(),
                self.to_currency.get()
            )

            if result:
                self.result_label.config(
                    text=f"{result['converted']:,.2f} {result['to_currency']}"
                )
                self._add_to_history(result)

        except:
            self.result_label.config(text="Invalid amount")

    def _add_to_history(self, data):

        if self.empty_label.winfo_exists():
            self.empty_label.destroy()

        item = tk.Frame(self.history_container, bg='white', bd=1, relief="solid")
        item.pack(fill="x", pady=5)

        tk.Label(
            item,
            text=f"{data['amount']} {data['from_currency']} → {data['converted']:,.2f} {data['to_currency']}",
            bg='white'
        ).pack(anchor="w", padx=10, pady=10)
