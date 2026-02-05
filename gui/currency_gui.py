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
