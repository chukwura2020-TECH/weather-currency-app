# gui/components/sidebar.py

import tkinter as tk
import os
from gui.styles.theme import COLORS
from gui.utils.icon_loader import load_icon


class Sidebar(tk.Frame):
    """Production-ready sidebar using PNG icons"""

    def __init__(self, parent, on_navigate):
        super().__init__(parent, bg=COLORS['bg_primary'], width=90)

        self.on_navigate = on_navigate
        self.pack_propagate(False)

        # Prevent image garbage collection
        self.icons = {}

        self._create_widgets()

    def _create_widgets(self):

        # ================= Logo =================
        logo_frame = tk.Frame(self, bg=COLORS['bg_primary'])
        logo_frame.pack(pady=25)

        logo_icon = load_icon(
            os.path.join("assets/icons", "cloud.png"),
            size=50,
            color="#ffffff"
        )

        self.icons["logo"] = logo_icon

        tk.Label(
            logo_frame,
            image=logo_icon,
            bg=COLORS['bg_primary']
        ).pack()

        # ================= Navigation =================
        nav_container = tk.Frame(self, bg=COLORS['bg_primary'])
        nav_container.pack(fill="x", expand=True)

        nav_items = [
            ("cloud.png", "weather"),
            ("money.png", "currency"),
            ("gear.png", "settings"),
        ]

        for icon_file, view in nav_items:
            self._create_nav_button(nav_container, icon_file, view)

    def _create_nav_button(self, parent, icon_file, view):

        container = tk.Frame(parent, bg=COLORS['bg_primary'], height=70)
        container.pack(fill="x")
        container.pack_propagate(False)

        icon_path = os.path.join("assets/icons", icon_file)

        icon = load_icon(
            icon_path,
            size=35,
            color="#ffffff"
        )

        self.icons[view] = icon

        btn = tk.Label(
            container,
            image=icon,
            bg=COLORS['bg_primary'],
            cursor="hand2"
        )

        btn.place(relx=0.5, rely=0.5, anchor="center")

        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS['accent_blue']))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORS['bg_primary']))
        btn.bind("<Button-1>", lambda e: self.on_navigate(view))