import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ZoomableCanvas(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = ttk.Label(self, text=title)
        self.title.pack()

        self.canvas = tk.Canvas(self, background='#808080', cursor="fleur")
        self.canvas.pack(fill='both', expand=True)

        self.image = None
        self.tk_img = None
        self.image_id = None
        self.scale = 1.0
        self.current_width = 0
        self.current_height = 0

        # Offset per il panning
        self.offset_x = 0
        self.offset_y = 0
        self.pan_start_x = 0
        self.pan_start_y = 0

        # Eventi
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)      # Windows/Mac
        self.canvas.bind("<Button-4>", lambda e: self.on_mousewheel(-1))  # Linux scroll su
        self.canvas.bind("<Button-5>", lambda e: self.on_mousewheel(1))   # Linux scroll giù
        self.canvas.bind("<Double-Button-1>", self.reset_zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)  # Mouse click sinistro
        self.canvas.bind("<B1-Motion>", self.do_pan)         # Trascinamento

    def on_mousewheel(self, event):
        ZOOM_FACTOR = 1.05
        if isinstance(event, int):
            delta = event
        else:
            delta = -1 if event.delta < 0 else 1

        new_scale = self.scale * (ZOOM_FACTOR ** delta)
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

        self.offset_x = 0
        self.offset_y = 0

        self.draw_image()

    def apply_zoom(self):
        if not self.image:
            return
        self.offset_x = 0
        self.offset_y = 0
        self.draw_image()

    def draw_image(self):
        img_width, img_height = self.image.size
        new_w = int(img_width * self.scale)
        new_h = int(img_height * self.scale)

        resized = self.image.resize((new_w, new_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x = (canvas_width - new_w) // 2 + self.offset_x
        y = (canvas_height - new_h) // 2 + self.offset_y

        self.canvas.delete('all')
        self.image_id = self.canvas.create_image(x, y, anchor='nw', image=self.tk_img)

        self.current_width = new_w
        self.current_height = new_h

    def on_canvas_resize(self, event):
        self.update_image_fit()

    def start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def do_pan(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.current_width <= canvas_width and self.current_height <= canvas_height:
            return  # Non permettere panning se l'immagine ci sta completamente

        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y

        self.offset_x += dx
        self.offset_y += dy

        self.pan_start_x = event.x
        self.pan_start_y = event.y

        # Calcola i limiti massimi/minimi del panning
        max_offset_x = (self.current_width - canvas_width) // 2
        max_offset_y = (self.current_height - canvas_height) // 2

        # Limita l'offset per non far vedere lo sfondo
        self.offset_x = max(-max_offset_x, min(self.offset_x, max_offset_x))
        self.offset_y = max(-max_offset_y, min(self.offset_y, max_offset_y))

        self.draw_image()

    def reset_zoom(self, event):
        self.update_image_fit()