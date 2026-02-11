# gui/components/loading.py
"""
Loading spinner component.
"""
import tkinter as tk

class LoadingSpinner(tk.Canvas):
    """Animated loading spinner"""
    
    def __init__(self, parent, size=50, **kwargs):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=kwargs.get('bg', 'white'),
            highlightthickness=0
        )
        
        self.size = size
        self.angle = 0
        self.is_running = False
        
        # Draw spinner circle
        self.arc = self.create_arc(
            10, 10, size-10, size-10,
            start=0,
            extent=300,
            outline='#4A90E2',
            width=4,
            style='arc'
        )
    
    def start(self):
        """Start spinning animation"""
        self.is_running = True
        self._animate()
    
    def stop(self):
        """Stop spinning animation"""
        self.is_running = False
    
    def _animate(self):
        """Rotate the spinner"""
        if not self.is_running:
            return
        
        self.angle = (self.angle + 10) % 360
        self.itemconfig(self.arc, start=self.angle)
        
        # Continue animation
        self.after(50, self._animate)