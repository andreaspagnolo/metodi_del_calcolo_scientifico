import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from scipy.fftpack import dct, idct
import os

def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

class DCTCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT2 Image Compressor")

        self.image = None
        self.compressed_image = None
        self.tk_original = None
        self.tk_compressed = None

        # Layout
        self.mainframe = ttk.Frame(root, padding="15")
        self.mainframe.grid(row=0, column=0, sticky="NSEW")

        # Titolo
        ttk.Label(
            self.mainframe,
            text="Progetto MCS - Compressione Immagini DCT2",
            font=("Helvetica", 16)
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # Bottone per caricare file
        self.file_label = ttk.Label(self.mainframe, text="Nessun file selezionato")
        self.file_label.grid(row=1, column=0, columnspan=3)

        ttk.Button(
            self.mainframe, text="Scegli Immagine BMP", command=self.choose_file
        ).grid(row=2, column=0, columnspan=3, pady=5)

        # Parametri F e d
        self.F_var = tk.IntVar(value=8)
        self.d_var = tk.IntVar(value=8)

        ttk.Label(self.mainframe, text="Dimensione blocchi F:").grid(row=3, column=0, sticky="E")
        self.F_spin = ttk.Spinbox(
            self.mainframe, from_=2, to=64, textvariable=self.F_var, width=5, command=self.update_d_limit
        )
        self.F_spin.grid(row=3, column=1, sticky="W")

        ttk.Label(self.mainframe, text="Soglia frequenze d:").grid(row=4, column=0, sticky="E")
        self.d_spin = ttk.Spinbox(
            self.mainframe, from_=0, to=126, textvariable=self.d_var, width=5
        )
        self.d_spin.grid(row=4, column=1, sticky="W")

        # Pulsante per applicare compressione
        self.apply_button = ttk.Button(
            self.mainframe, text="Applica compressione", command=self.apply_compression, state="disabled"
        )
        self.apply_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Canvas per mostrare immagini
        self.canvas_frame = ttk.Frame(self.mainframe)
        self.canvas_frame.grid(row=6, column=0, columnspan=3)

        self.orig_label = ttk.Label(self.canvas_frame, text="Originale")
        self.orig_label.grid(row=0, column=0, padx=10)

        self.comp_label = ttk.Label(self.canvas_frame, text="Compressa")
        self.comp_label.grid(row=0, column=1, padx=10)

        self.orig_canvas = ttk.Label(self.canvas_frame)
        self.orig_canvas.grid(row=1, column=0, padx=10)

        self.comp_canvas = ttk.Label(self.canvas_frame)
        self.comp_canvas.grid(row=1, column=1, padx=10)

    def choose_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Bitmap Images", "*.bmp")])
        if filepath:
            try:
                img = Image.open(filepath).convert('L')
                self.image = img
                self.file_label.config(text=os.path.basename(filepath))
                self.show_image(self.orig_canvas, img, is_original=True)
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
        self.show_image(self.comp_canvas, img_comp, is_original=False)

    def show_image(self, canvas, img, is_original):
        img_resized = img.copy()
        img_resized.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img_resized)
        canvas.config(image=tk_img)
        canvas.image = tk_img

if __name__ == "__main__":
    root = tk.Tk()
    app = DCTCompressorApp(root)
    root.mainloop()
