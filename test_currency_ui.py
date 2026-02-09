# test_currency_ui.py
import tkinter as tk
from gui.currency_gui import CurrencyConverter

root = tk.Tk()
root.title("Currency Converter Test")
root.geometry("800x600")

converter = CurrencyConverter(root)
converter.pack(fill="both", expand=True)

root.mainloop()