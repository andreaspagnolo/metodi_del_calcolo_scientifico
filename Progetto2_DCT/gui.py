import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os

from utils import ZoomableCanvas
from core import compress_image

class DCTCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCT2 Image Compressor")
        self.root.geometry("1200x700")

        self.image = None
        self.compressed_image = None

        self.mainframe = ttk.Frame(root, padding="15")
        self.mainframe.pack(fill='both', expand=True)

        ttk.Label(
            self.mainframe,
            text="Progetto MCS - Compressione Immagini DCT2",
            font=("Helvetica", 16)
        ).pack(pady=10)

        top_frame = ttk.Frame(self.mainframe)
        top_frame.pack()

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)

        self.file_label = ttk.Label(top_frame, text="Nessun file selezionato")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky='nsew')

        ttk.Button(
            top_frame, text="Scegli Immagine BMP", command=self.choose_file
        ).grid(row=1, column=0, columnspan=3, pady=5, sticky='nsew')

        ttk.Label(top_frame, text="Dimensione blocchi F:").grid(row=2, column=0, sticky="E")
        self.F_var = tk.IntVar(value=8)
        self.F_spin = ttk.Spinbox(
            top_frame, from_=2, to=1000, textvariable=self.F_var, width=5, command=self.update_d_limit
        )
        self.F_spin.grid(row=2, column=1, sticky="W")

        ttk.Label(top_frame, text="Soglia frequenze d:").grid(row=3, column=0, sticky="E")
        self.d_var = tk.IntVar(value=8)
        self.d_spin = ttk.Spinbox(
            top_frame, from_=0, to=1000, textvariable=self.d_var, width=5
        )
        self.d_spin.grid(row=3, column=1, sticky="W")

        self.apply_button = ttk.Button(
            top_frame, text="Applica compressione", command=self.apply_compression, state="disabled"
        )
        self.apply_button.grid(row=4, column=0, columnspan=3, pady=10)

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

                # Calcola limiti dinamici per F
                w, h = img.size
                max_F = min(w, h)
                max_F = max(2, max_F)
                self.F_spin.config(to=max_F)
                if self.F_var.get() > max_F:
                    self.F_var.set(max_F)

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
        F = self.F_var.get()
        w, h = self.image.size
        max_F = min(w, h)
        if F > max_F:
            messagebox.showerror("Errore", f"\"F\" troppo grande. Massimo consentito: {max_F}")
            return
        if self.image is None:
            return

        d = self.d_var.get()
        max_d = 2 * max_F - 2 
        if d > max_d:
            messagebox.showerror("Errore", f"\"d\" troppo grande. Massimo consentito: {max_d}")
            return
        if self.image is None:
            return

        arr_comp = compress_image(self.image, F, d)
        img_comp = Image.fromarray(arr_comp)
        self.compressed_image = img_comp
        self.comp_canvas.display_image(img_comp)

if __name__ == "__main__":
    root = tk.Tk()
    app = DCTCompressorApp(root)
    root.mainloop()
