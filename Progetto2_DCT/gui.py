import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from scipy.fftpack import dctn, idctn
import os

def dct2(block):
    return dctn(block, type=2, norm='ortho')

def idct2(block):
    return idctn(block, type=2, norm='ortho')

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
        # Fattore di zoom molto piccolo (1.05 = 5% per scatto)
        ZOOM_FACTOR = 1.05
        
        # Determina direzione (gestisce tutti i sistemi operativi)
        if isinstance(event, int):  # Per i binding Linux
            delta = event
        else:                      # Per Windows/Mac
            delta = -1 if event.delta < 0 else 1
        
        # Calcola nuovo zoom con limiti (0.1x - 10x)
        new_scale = self.scale * (ZOOM_FACTOR ** (-delta))
        self.scale = max(0.1, min(10.0, new_scale))
        
        self.apply_zoom()
        return "break"  # Previene lo scrolling del canvas

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

        # Controlla se l'immagine è più grande del canvas in almeno una dimensione
        if img_width > canvas_width or img_height > canvas_height:
            # Calcola il fattore di scala per adattare l'immagine al canvas
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            self.scale = min(scale_w, scale_h)
        else:
            # Immagine più piccola: mostra a dimensione naturale
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


class DCTCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT2 Image Compressor")
        self.root.geometry("1200x700")  # finestra più grande

        self.image = None
        self.compressed_image = None

        # Layout principale
        self.mainframe = ttk.Frame(root, padding="15")
        self.mainframe.pack(fill='both', expand=True)

        ttk.Label(
            self.mainframe,
            text="Progetto MCS - Compressione Immagini DCT2",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Selezione file e parametri
        top_frame = ttk.Frame(self.mainframe)
        top_frame.pack()

        self.file_label = ttk.Label(top_frame, text="Nessun file selezionato")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky='w')

        ttk.Button(
            top_frame, text="Scegli Immagine BMP", command=self.choose_file
        ).grid(row=1, column=0, pady=5)

        ttk.Label(top_frame, text="Dimensione blocchi F:").grid(row=2, column=0, sticky="E")
        self.F_var = tk.IntVar(value=8)
        self.F_spin = ttk.Spinbox(
            top_frame, from_=2, to=64, textvariable=self.F_var, width=5, command=self.update_d_limit
        )
        self.F_spin.grid(row=2, column=1, sticky="W")

        ttk.Label(top_frame, text="Soglia frequenze d:").grid(row=3, column=0, sticky="E")
        self.d_var = tk.IntVar(value=8)
        self.d_spin = ttk.Spinbox(
            top_frame, from_=0, to=126, textvariable=self.d_var, width=5
        )
        self.d_spin.grid(row=3, column=1, sticky="W")

        self.apply_button = ttk.Button(
            top_frame, text="Applica compressione", command=self.apply_compression, state="disabled"
        )
        self.apply_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Canvases zoomabili
        canvas_frame = ttk.Frame(self.mainframe)
        canvas_frame.pack(fill='both', expand=True)

        self.orig_canvas = ZoomableCanvas(canvas_frame, "Originale")
        self.orig_canvas.pack(side='left', fill='both', expand=True, padx=5)

        self.comp_canvas = ZoomableCanvas(canvas_frame, "Compressa")
        self.comp_canvas.pack(side='left', fill='both', expand=True, padx=5)

    def choose_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Bitmap Images", "*.bmp")])
        if filepath:
            try:
                img = Image.open(filepath).convert('L')
                self.image = img
                self.file_label.config(text=os.path.basename(filepath))
                self.orig_canvas.display_image(img)
                self.apply_button.config(state="normal")
                self.update_d_limit()
            except:
                messagebox.showerror("Errore", "Immagine non valida")

    def update_d_limit(self):
        F = self.F_var.get()
        max_d = 2 * F - 2
        self.d_spin.config(to=max_d)
        if self.d_var.get() > max_d:
            self.d_var.set(max_d)

    def apply_compression(self):
        if self.image is None:
            return

        F = self.F_var.get()
        d = self.d_var.get()

        arr = np.array(self.image, dtype=np.float64)
        h, w = arr.shape

        w = w - (w % F)
        h = h - (h % F)
        arr = arr[:h, :w]
        arr_comp = np.zeros_like(arr)

        for i in range(0, h, F):
            for j in range(0, w, F):
                block = arr[i:i+F, j:j+F]
                coeffs = dct2(block)
                for k in range(F):
                    for l in range(F):
                        if k + l >= d:
                            coeffs[k, l] = 0
                block_rec = idct2(coeffs)
                block_rec = np.round(block_rec)
                block_rec[block_rec < 0] = 0
                block_rec[block_rec > 255] = 255
                arr_comp[i:i+F, j:j+F] = block_rec

        img_comp = Image.fromarray(arr_comp.astype(np.uint8))
        self.compressed_image = img_comp
        self.comp_canvas.display_image(img_comp)

if __name__ == "__main__":
    root = tk.Tk()
    app = DCTCompressorApp(root)
    root.mainloop()



class DCTCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT2 Image Compressor")
        self.root.geometry("1200x700")  # finestra più grande

        self.image = None
        self.compressed_image = None

        # Layout principale
        self.mainframe = ttk.Frame(root, padding="15")
        self.mainframe.pack(fill='both', expand=True)

        ttk.Label(
            self.mainframe,
            text="Progetto MCS - Compressione Immagini DCT2",
            font=("Helvetica", 16)
        ).pack(pady=10)

        # Selezione file e parametri
        top_frame = ttk.Frame(self.mainframe)
        top_frame.pack()

        self.file_label = ttk.Label(top_frame, text="Nessun file selezionato")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky='w')

        ttk.Button(
            top_frame, text="Scegli Immagine BMP", command=self.choose_file
        ).grid(row=1, column=0, pady=5)

        ttk.Label(top_frame, text="Dimensione blocchi F:").grid(row=2, column=0, sticky="E")
        self.F_var = tk.IntVar(value=8)
        self.F_spin = ttk.Spinbox(
            top_frame, from_=2, to=64, textvariable=self.F_var, width=5, command=self.update_d_limit
        )
        self.F_spin.grid(row=2, column=1, sticky="W")

        ttk.Label(top_frame, text="Soglia frequenze d:").grid(row=3, column=0, sticky="E")
        self.d_var = tk.IntVar(value=8)
        self.d_spin = ttk.Spinbox(
            top_frame, from_=0, to=126, textvariable=self.d_var, width=5
        )
        self.d_spin.grid(row=3, column=1, sticky="W")

        self.apply_button = ttk.Button(
            top_frame, text="Applica compressione", command=self.apply_compression, state="disabled"
        )
        self.apply_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Canvases zoomabili
        canvas_frame = ttk.Frame(self.mainframe)
        canvas_frame.pack(fill='both', expand=True)

        self.orig_canvas = ZoomableCanvas(canvas_frame, "Originale")
        self.orig_canvas.pack(side='left', fill='both', expand=True, padx=5)

        self.comp_canvas = ZoomableCanvas(canvas_frame, "Compressa")
        self.comp_canvas.pack(side='left', fill='both', expand=True, padx=5)

    def choose_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Bitmap Images", "*.bmp")])
        if filepath:
            try:
                img = Image.open(filepath).convert('L')
                self.image = img
                self.file_label.config(text=os.path.basename(filepath))
                self.orig_canvas.display_image(img)
                self.apply_button.config(state="normal")
                self.update_d_limit()
            except:
                messagebox.showerror("Errore", "Immagine non valida")

    def update_d_limit(self):
        F = self.F_var.get()
        max_d = 2 * F - 2
        self.d_spin.config(to=max_d)
        if self.d_var.get() > max_d:
            self.d_var.set(max_d)

    def apply_compression(self):
        if self.image is None:
            return

        F = self.F_var.get()
        d = self.d_var.get()

        arr = np.array(self.image, dtype=np.float64)
        h, w = arr.shape

        w = w - (w % F)
        h = h - (h % F)
        arr = arr[:h, :w]
        arr_comp = np.zeros_like(arr)

        for i in range(0, h, F):
            for j in range(0, w, F):
                block = arr[i:i+F, j:j+F]
                coeffs = dct2(block)
                for k in range(F):
                    for l in range(F):
                        if k + l >= d:
                            coeffs[k, l] = 0
                block_rec = idct2(coeffs)
                block_rec = np.round(block_rec)
                block_rec[block_rec < 0] = 0
                block_rec[block_rec > 255] = 255
                arr_comp[i:i+F, j:j+F] = block_rec

        img_comp = Image.fromarray(arr_comp.astype(np.uint8))
        self.compressed_image = img_comp
        self.comp_canvas.display_image(img_comp)

if __name__ == "__main__":
    root = tk.Tk()
    app = DCTCompressorApp(root)
    root.mainloop()

