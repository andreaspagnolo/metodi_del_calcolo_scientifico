# Progetto 2 - Compressione di immagini tramite la DCT

**Anno Accademico 2024-2025 – Metodi del Calcolo Scientifico**  
Autori: [andreaspagnolo](https://github.com/andreaspagnolo)  e [davidefalanga01](https://github.com/davidefalanga01)

---

## 📌 Descrizione

Questo progetto esplora l'utilizzo della Trasformata Discreta del Coseno bidimensionale (DCT2) per la **compressione di immagini in scala di grigi**, secondo una versione semplificata del metodo JPEG (senza matrice di quantizzazione).

Il lavoro è suddiviso in **due parti**:

1. Implementazione della DCT2 e confronto dei tempi di esecuzione con la versione ottimizzata di libreria.
2. Realizzazione di un software interattivo per la compressione di immagini.

---

## 🧪 Parte 1 – DCT2: Implementazione e Benchmark

- Implementazione manuale della DCT2 (`O(N³)`) secondo quanto spiegato a lezione.
- Confronto delle performance con la DCT2 della libreria `scipy.fft.dctn` (`O(N² log N)`).
- Esperimenti su array `N x N` con `N` crescente.
- Produzione di un **grafico in scala semilogaritmica** (ascisse lineari, ordinate logaritmiche) che confronta i tempi.

---

## 🖼️ Parte 2 – Compressione di immagini tramite blocchi DCT

### Funzionalità

- Selezione di un file `.bmp` in **toni di grigio** tramite interfaccia grafica (`tkinter`).
- Parametri configurabili:
  - `F`: dimensione del blocco (`F x F`)
  - `d`: soglia per il taglio delle frequenze (`0 ≤ d ≤ 2F−2`)
- Compressione dell’immagine mediante:
  - suddivisione in blocchi `F x F`
  - applicazione della DCT2
  - **eliminazione** dei coefficienti con `k + ℓ ≥ d`
  - IDCT2 per ricostruzione dei blocchi
  - ricostruzione e visualizzazione dell’immagine compressa

### Output

- Visualizzazione comparativa:
  - 📷 Immagine originale
  - 🧊 Immagine compressa

---
## Struttura del progetto  
Progetto2_DCT/  
│  
├── dct.ipynb&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Implementazione manuale DCT2 e comparazione con scipy.fft.dctn  
├── core.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Compressione per blocchi e nucleo matematico  
├── gui.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Interfaccia grafica (Tkinter)  
├── utils.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Implementazione ZoomableCanvas util  
└── README.md           


## 🛠️ Requisiti

Le seguenti librerie Python:

```bash
pip install numpy scipy matplotlib pillow
```
Per l'esecuzione del software:  
```bash
python gui.py
```
