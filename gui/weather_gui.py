import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "YOUR_API_KEY"


class WeatherFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="🌤 Weather", font=("Arial", 18)).pack(pady=12)

        tk.Button(
            self,
            text="Go to Currency",
            command=lambda: controller.show_frame("CurrencyFrame")
        ).pack()

        tk.Button(
            self,
            text="Map View",
            command=lambda: controller.show_frame("MapFrame")
        ).pack(pady=4)

        tk.Label(self, text="Enter City:").pack(pady=8)

        self.city_entry = tk.Entry(self, width=25)
        self.city_entry.pack()

        tk.Button(
            self,
            text="Check Weather",
            command=self.get_weather
        ).pack(pady=10)

        self.result_label = tk.Label(self, font=("Arial", 12))
        self.result_label.pack(pady=12)

    def get_weather(self):
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning("Input Error", "Enter a city name.")
            return

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code != 200:
                messagebox.showerror("Error", data.get("message", "City not found"))
                return

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].title()
            humidity = data["main"]["humidity"]

            self.result_label.config(
                text=(
                    f"City: {city.title()}\n"
                    f"Temperature: {temp}°C\n"
                    f"Condition: {desc}\n"
                    f"Humidity: {humidity}%"
                )
            )

        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "Failed to connect to API.")
