# gui/components/loading.py
"""
Animated loading spinner component.
NOW WITH REAL ANIMATION! 🔄
"""
import tkinter as tk
from gui.styles.theme import COLORS
import math

class LoadingSpinner(tk.Canvas):
    """Animated circular loading spinner"""
    
    def __init__(self, parent, size=50, line_width=4, speed=100):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=COLORS['bg_card'],
            highlightthickness=0
        )
        
        self.size = size
        self.line_width = line_width
        self.speed = speed
        self.angle = 0
        self.is_spinning = False
        self.animation_id = None
        
        self.center_x = size // 2
        self.center_y = size // 2
        self.radius = (size - line_width) // 2
        
        # Create the arc
        self.arc = self.create_arc(
            line_width, line_width,
            size - line_width, size - line_width,
            start=0, extent=270,
            outline=COLORS['accent_blue'],
            width=line_width,
            style=tk.ARC
        )
    
    def start(self):
        """Start the spinning animation"""
        if not self.is_spinning:
            self.is_spinning = True
            self._animate()
    
    def stop(self):
        """Stop the spinning animation"""
        self.is_spinning = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
    
    def _animate(self):
        """Animate the spinner rotation"""
        if not self.is_spinning:
            return
        
        # Update rotation angle
        self.angle = (self.angle + 10) % 360
        
        # Update arc position
        self.itemconfig(self.arc, start=self.angle)
        
        # Schedule next frame
        self.animation_id = self.after(self.speed, self._animate)
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.itemconfig(self.arc, outline=COLORS['accent_blue'])


class LoadingOverlay(tk.Frame):
    """Full-screen loading overlay with spinner and message"""
    
    def __init__(self, parent, message="Loading..."):
        super().__init__(parent, bg='#000000')
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Semi-transparent background effect (can't do real transparency in tkinter)
        self.config(bg='#F7FAFC')
        
        # Container
        container = tk.Frame(self, bg=COLORS['bg_card'])
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Spinner
        self.spinner = LoadingSpinner(container, size=60, line_width=5, speed=50)
        self.spinner.pack(pady=20, padx=40)
        
        # Message
        self.message_label = tk.Label(
            container,
            text=message,
            bg=COLORS['bg_card'],
            fg=COLORS['text_dark'],
            font=('Segoe UI', 14)
        )
        self.message_label.pack(pady=(0, 20), padx=40)
        
        # Start spinning
        self.spinner.start()
    
    def show(self, message=None):
        """Show the loading overlay"""
        if message:
            self.message_label.config(text=message)
        self.lift()
        self.spinner.start()
    
    def hide(self):
        """Hide the loading overlay"""
        self.spinner.stop()
        self.place_forget()
    
    def update_colors(self):
        """Update colors when theme changes"""
        self.config(bg=COLORS['bg_card'])
        self.spinner.update_colors()
        self.message_label.config(bg=COLORS['bg_card'], fg=COLORS['text_dark'])