import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ZoomableCanvas(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = ttk.Label(self, text=title)
        self.title.pack()

        self.canvas = tk.Canvas(self, background='#808080')
        self.canvas.pack(fill='both', expand=True)

        self.image = None
        self.tk_img = None
        self.scale = 1.0
        self.current_width = 0
        self.current_height = 0

        # Binding per eventi
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)      # Windows/Mac
        self.canvas.bind("<Button-4>", lambda e: self.on_mousewheel(-1))  # Linux (rotella su)
        self.canvas.bind("<Button-5>", lambda e: self.on_mousewheel(1))   # Linux (rotella giù)

    def on_mousewheel(self, event):
        ZOOM_FACTOR = 1.05

        if isinstance(event, int):
            delta = event
        else:
            delta = -1 if event.delta < 0 else 1

        new_scale = self.scale * (ZOOM_FACTOR ** (delta))
        self.scale = max(0.1, min(10.0, new_scale))

        self.apply_zoom()
        return "break"

    def display_image(self, pil_img):
        self.image = pil_img
        self.update_image_fit()

    def update_image_fit(self):
        if not self.image:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.after(100, self.update_image_fit)
            return

        img_width, img_height = self.image.size

        if img_width > canvas_width or img_height > canvas_height:
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            self.scale = min(scale_w, scale_h)
        else:
            self.scale = 1.0

        new_w = int(img_width * self.scale)
        new_h = int(img_height * self.scale)

        resized = self.image.resize((new_w, new_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)

        self.canvas.delete('all')
        x = (canvas_width - new_w) // 2
        y = (canvas_height - new_h) // 2
        self.canvas.create_image(x, y, anchor='nw', image=self.tk_img)

        self.current_width = new_w
        self.current_height = new_h

    def on_canvas_resize(self, event):
        self.update_image_fit()

    def apply_zoom(self):
        if not self.image:
            return

        img_width, img_height = self.image.size
        new_w = int(img_width * self.scale)
        new_h = int(img_height * self.scale)

        resized = self.image.resize((new_w, new_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = max((canvas_width - new_w) // 2, 0)
        y = max((canvas_height - new_h) // 2, 0)
        self.canvas.delete('all')
        self.canvas.create_image(x, y, anchor='nw', image=self.tk_img)
