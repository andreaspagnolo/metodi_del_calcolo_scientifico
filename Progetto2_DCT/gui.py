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
        self.updating_params = False  # Flag per evitare loop infiniti

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

        self.F_label = ttk.Label(top_frame, text="Dimensione blocchi F:")
        self.F_label.grid(row=2, column=0, sticky="E")
        self.F_var = tk.IntVar(value=8)
        self.F_spin = ttk.Spinbox(
            top_frame, from_=2, to=1000, textvariable=self.F_var, width=5, 
            command=self.on_F_changed
        )
        self.F_spin.grid(row=2, column=1, sticky="W")



        self.d_label = ttk.Label(top_frame, text="Soglia frequenze d:")
        self.d_label.grid(row=3, column=0, sticky="E")
        self.d_var = tk.IntVar(value=8)
        self.d_spin = ttk.Spinbox(
            top_frame, from_=0, to=1000, textvariable=self.d_var, width=5,
            command=self.on_d_changed
        )
        self.d_spin.grid(row=3, column=1, sticky="W")

        # Label per mostrare il range valido di d
        self.d_range_label = ttk.Label(top_frame, text="(0 ≤ d ≤ ?)", font=(12))
        self.d_range_label.grid(row=3, column=2, sticky="W", padx=(5, 0))

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

        # Associa i trace agli IntVar DOPO aver creato tutte le etichette
        self.F_var.trace_add("write", self.on_F_trace)
        self.d_var.trace_add("write", self.on_d_trace)

        # Inizializza i controlli
        self.update_parameter_limits()

    def choose_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Bitmap Images", "*.bmp")])
        if filepath:
            try:
                img = Image.open(filepath).convert('L')
                self.image = img
                self.file_label.config(text=os.path.basename(filepath))
                self.orig_canvas.display_image(img)
                
                # Aggiorna i limiti dei parametri in base alle dimensioni dell'immagine
                self.update_parameter_limits()
                
            except Exception as e:
                messagebox.showerror("Errore", f"Immagine non valida: {str(e)}")

    def get_F_limits(self):
        """Calcola i limiti validi per F"""
        if self.image is None:
            return 2, 1000  # Valori di default
        
        w, h = self.image.size
        max_F = min(w, h)
        return 2, max(2, max_F)

    def get_d_limits(self, F):
        """Calcola i limiti validi per d dato un valore di F"""
        max_d = 2 * F - 2
        return 0, max_d

    def update_parameter_limits(self):
        """Aggiorna i limiti dei controlli Spinbox e le etichette informative"""
        if self.updating_params:
            return
        
        self.updating_params = True
        
        try:
            # Aggiorna i limiti di F
            min_F, max_F = self.get_F_limits()
            self.F_spin.config(from_=min_F, to=max_F)
            
            # Assicurati che F sia nei limiti validi
            current_F = self.F_var.get()
            if current_F < min_F:
                self.F_var.set(min_F)
                current_F = min_F
            elif current_F > max_F:
                self.F_var.set(max_F)
                current_F = max_F
            
            # Aggiorna i limiti di d in base al valore corrente di F
            min_d, max_d = self.get_d_limits(current_F)
            self.d_spin.config(from_=min_d, to=max_d)
            self.d_range_label.config(text=f"({min_d} ≤ d ≤ {max_d})")
            
            # Assicurati che d sia nei limiti validi
            current_d = self.d_var.get()
            if current_d < min_d:
                self.d_var.set(min_d)
            elif current_d > max_d:
                self.d_var.set(max_d)
            
            # Valida lo stato del pulsante
            self.validate_parameters()
            
        finally:
            self.updating_params = False

    def on_F_changed(self):
        """Chiamato quando F viene modificato tramite i pulsanti del Spinbox"""
        if not self.updating_params:
            self.update_parameter_limits()

    def on_d_changed(self):
        """Chiamato quando d viene modificato tramite i pulsanti del Spinbox"""
        if not self.updating_params:
            self.validate_parameters()

    def on_F_trace(self, *args):
        """Chiamato quando F viene modificato (anche tramite digitazione)"""
        if not self.updating_params:
            # Usa after per evitare problemi con la validazione durante la digitazione
            self.root.after_idle(self.update_parameter_limits)

    def on_d_trace(self, *args):
        """Chiamato quando d viene modificato (anche tramite digitazione)"""
        if not self.updating_params:
            self.root.after_idle(self.validate_parameters)

    def validate_parameters(self):
        """Valida i parametri correnti e abilita/disabilita il pulsante di applicazione"""
        if self.image is None:
            self.apply_button.config(state="disabled")
            # Ripristina i colori normali quando non c'è immagine
            self.F_label.config(foreground="white")
            self.d_label.config(foreground="white")
            return False

        try:
            F = self.F_var.get()
            d = self.d_var.get()
            
            # Verifica i limiti di F
            min_F, max_F = self.get_F_limits()
            if F < min_F or F > max_F:
                self.apply_button.config(state="disabled")
                self.F_label.config(foreground="red")
                self.d_label.config(foreground="black")  # Ripristina d se F è errato
                return False
            else:
                self.F_label.config(foreground="black")
            
            # Verifica i limiti di d
            min_d, max_d = self.get_d_limits(F)
            if d < min_d or d > max_d:
                self.apply_button.config(state="disabled")
                self.d_label.config(foreground="red")
                return False
            else:
                self.d_label.config(foreground="black")
            
            self.apply_button.config(state="normal")
            return True
            
        except (ValueError, tk.TclError):
            self.apply_button.config(state="disabled")
            # In caso di errore di parsing, colora entrambi di rosso
            self.F_label.config(foreground="red")
            self.d_label.config(foreground="red")
            return False

    def apply_compression(self):
        if self.image is None:
            return

        if not self.validate_parameters():
            messagebox.showerror("Errore", "Parametri non validi")
            return

        F = self.F_var.get()
        d = self.d_var.get()

        try:
            arr_comp = compress_image(self.image, F, d)
            img_comp = Image.fromarray(arr_comp)
            self.compressed_image = img_comp
            self.comp_canvas.display_image(img_comp)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la compressione: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DCTCompressorApp(root)
    root.mainloop()