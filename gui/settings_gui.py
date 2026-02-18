# gui/settings_gui.py
"""
Settings page with actual functionality!
🐛 FIXED: Temperature unit selector now works!
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.styles.theme import COLORS, FONTS, DIMENSIONS, is_dark_mode
from utils.favorites import load_favorites, clear_favorites
import json
import os

# File to persist the temperature unit preference
SETTINGS_FILE = 'settings.json'

def load_settings():
    """Load saved settings from file"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {"temp_unit": "Celsius"}  # Default

def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Failed to save settings: {e}")

class SettingsPage(tk.Frame):
    """Settings and preferences page"""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.settings = load_settings()
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings UI"""
        
        # Title
        title = tk.Label(
            self,
            text="Settings",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_white'],
            font=FONTS['title']
        )
        title.pack(pady=(40, 30))
        
        # Settings container
        settings_container = tk.Frame(self, bg='white')
        settings_container.pack(padx=50, pady=20, fill="both", expand=True)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(settings_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(settings_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Content padding
        content = tk.Frame(scrollable_frame, bg='white')
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        # SECTION 1: Appearance
        self._create_section(content, "🎨 Appearance")
        
        # Theme info
        theme_frame = tk.Frame(content, bg='white')
        theme_frame.pack(fill="x", pady=(0, 20))
        
        current_theme = "Dark Mode" if is_dark_mode() else "Light Mode"
        tk.Label(
            theme_frame,
            text=f"Current Theme: {current_theme}",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body']
        ).pack(anchor="w")
        
        tk.Label(
            theme_frame,
            text="💡 Use the toggle button in the sidebar to switch themes",
            bg='white',
            fg=COLORS['text_muted'],
            font=FONTS['small']
        ).pack(anchor="w", pady=(5, 0))
        
        # SECTION 2: Weather Settings
        self._create_section(content, "🌤️ Weather Settings")
        
        # Temperature unit
        unit_frame = tk.Frame(content, bg='white')
        unit_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            unit_frame,
            text="Temperature Unit:",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body_bold']
        ).pack(anchor="w", pady=(0, 10))

        # Load saved preference
        self.temp_unit = tk.StringVar(value=self.settings.get("temp_unit", "Celsius"))

        for unit in ["Celsius", "Fahrenheit"]:
            rb = tk.Radiobutton(
                unit_frame,
                text=unit,
                variable=self.temp_unit,
                value=unit,
                bg='white',
                fg=COLORS['text_dark'],
                font=FONTS['body'],
                selectcolor='#E8F4FD',
                activebackground='white',
                command=self._on_unit_change  # ✅ Fires when selection changes
            )
            rb.pack(anchor="w", pady=2)

        # Live feedback label
        self.unit_feedback = tk.Label(
            unit_frame,
            text=f"✅ Currently set to: {self.temp_unit.get()}",
            bg='white',
            fg='#48BB78',
            font=FONTS['small']
        )
        self.unit_feedback.pack(anchor="w", pady=(8, 0))
        
        # SECTION 3: Favorites Management
        self._create_section(content, "⭐ Favorites Management")
        
        favorites = load_favorites()
        
        fav_info = tk.Label(
            content,
            text=f"You have {len(favorites)} favorite cities saved",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body']
        )
        fav_info.pack(anchor="w", pady=(0, 10))
        
        if favorites:
            tk.Label(
                content,
                text=", ".join(favorites),
                bg='white',
                fg=COLORS['text_muted'],
                font=FONTS['small'],
                wraplength=600
            ).pack(anchor="w", pady=(0, 15))
        
        clear_btn = tk.Button(
            content,
            text="🗑️ Clear All Favorites",
            bg='#E53E3E',
            fg='white',
            font=FONTS['body_bold'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._clear_favorites,
            activebackground='#C53030'
        )
        clear_btn.pack(anchor="w", pady=(0, 20))
        
        # SECTION 4: About
        self._create_section(content, "ℹ️ About")
        
        about_text = """
Weather & Currency Dashboard
Version 2.0 - Enhanced Edition

Created by: Victor, Millicente, Goodness, Ekene

Features:
✅ Real-time weather data
✅ 5-day forecast
✅ Currency converter (40+ currencies)
✅ Dark mode
✅ Interactive weather map
✅ Temperature charts
✅ Weather alerts
✅ Favorite cities

Powered by:
• OpenWeatherMap API
• ExchangeRate-API
        """
        
        tk.Label(
            content,
            text=about_text.strip(),
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body'],
            justify='left'
        ).pack(anchor="w", pady=(0, 20))
        
        # SECTION 5: Data & Cache
        self._create_section(content, "💾 Data & Cache")
        
        tk.Label(
            content,
            text="Clear cached data and reset app to defaults",
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['body']
        ).pack(anchor="w", pady=(0, 10))
        
        reset_btn = tk.Button(
            content,
            text="🔄 Reset App",
            bg=COLORS['accent_light'],
            fg=COLORS['text_dark'],
            font=FONTS['body_bold'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self._reset_app,
            activebackground='#CBD5E0'
        )
        reset_btn.pack(anchor="w")

    def _on_unit_change(self):
        """Called when temperature unit radio button is changed"""
        selected = self.temp_unit.get()

        # Update feedback label
        self.unit_feedback.config(text=f"✅ Currently set to: {selected}")

        # Save preference to file
        self.settings["temp_unit"] = selected
        save_settings(self.settings)

    def _create_section(self, parent, title):
        """Create a section header"""
        section_frame = tk.Frame(parent, bg='white')
        section_frame.pack(fill="x", pady=(20, 10))
        
        tk.Label(
            section_frame,
            text=title,
            bg='white',
            fg=COLORS['text_dark'],
            font=FONTS['heading']
        ).pack(anchor="w")
        
        # Divider line
        tk.Frame(
            section_frame,
            bg=COLORS['border_light'],
            height=2
        ).pack(fill="x", pady=(10, 0))
    
    def _clear_favorites(self):
        """Clear all favorite cities"""
        if messagebox.askyesno(
            "Clear Favorites",
            "Are you sure you want to remove all favorite cities?"
        ):
            clear_favorites()
            messagebox.showinfo("Success", "All favorites have been cleared!")
            
            # Refresh the page
            self.destroy()
            self.__init__(self.master)
            self.pack(fill="both", expand=True)
    
    def _reset_app(self):
        """Reset app to defaults"""
        if messagebox.askyesno(
            "Reset App",
            "This will clear all favorites and cached data. Continue?"
        ):
            try:
                # Clear favorites
                clear_favorites()
                
                # Clear favorites.json
                with open('favorites.json', 'w') as f:
                    json.dump([], f)

                # Reset settings
                save_settings({"temp_unit": "Celsius"})
                self.temp_unit.set("Celsius")
                self.unit_feedback.config(text="✅ Currently set to: Celsius")
                
                messagebox.showinfo("Success", "App has been reset to defaults!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset: {e}")
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_primary'])