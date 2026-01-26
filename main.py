# main.py
"""
Entry point for the Weather Dashboard application.
"""
import tkinter as tk
from gui.main_gui import WeatherApp

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()