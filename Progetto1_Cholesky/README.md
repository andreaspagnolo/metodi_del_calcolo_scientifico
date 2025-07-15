# Metodi del Calcolo Scientifico – Progetto 1

**Anno Accademico 2024-2025 – Metodi del Calcolo Scientifico**  
Autori: [andreaspagnolo](https://github.com/andreaspagnolo)  e [davidefalanga01](https://github.com/davidefalanga01)

---

## 📌 Descrizione del progetto

Questo progetto ha l’obiettivo di studiare e confrontare l’implementazione del **metodo di Cholesky** per la risoluzione di sistemi lineari con matrici sparse, simmetriche e definite positive, utilizzando:
- **MATLAB** (software proprietario)
- Una libreria **open source** a scelta (in questo caso implementazione in **Python**)

Il confronto avviene su:
- Sistemi operativi **Linux** e **Windows**
- Stessa macchina hardware

Vengono confrontati:
- **Tempo di calcolo**
- **Errore relativo**
- **Memoria utilizzata**
- **Facilità d’uso** e **documentazione** degli strumenti

---

## ⚙️ Struttura del repository
├── .gitignore  
├── README.md  
├── cholesky.py  
├── cholesnki.m  
└── comparison_plots.py  

- **cholesnki.m**: Implementazione MATLAB del metodo di Cholesky
- **cholesky.py**: Implementazione Python del metodo di Cholesky
- **comparison_plots.py**: Script per generare i grafici di confronto (tempo, errore, memoria)

---

## 🗂️ Dataset di matrici sparse

Le matrici di test provengono dalla **SuiteSparse Matrix Collection**:  
https://sparse.tamu.edu/

Esempi di matrici utilizzate:
- Flan 1565
- StocF-1465
- cfd1, cfd2
- G3_circuit
- parabolic_fem
- apache2
- shallow_water1
- ex15

---

## 🔬 Metodo di lavoro

1️⃣ **Generazione del sistema**:  
Per ciascuna matrice $A$, si risolve il sistema $Ax = b$ con termine noto $b = A \cdot x_e$, dove $x_e$ è un vettore noto di tutti 1.

2️⃣ **Calcolo**:
- Tempo di risoluzione
- Errore relativo:  
  $$ errore = \\frac{ \\| x - x_e \\|_2 }{ \\| x_e \\|_2 } $$

- Memoria impiegata: differenza di memoria prima e dopo la risoluzione.

3️⃣ **Visualizzazione risultati**:  
I risultati sono riportati in grafici con:
- Ascissa = nome della matrice (in ordine di dimensione)
- Ordinata (scala logaritmica) = tempo, errore, memoria

---

## 📊 Confronto

Per ogni combinazione **(software, sistema operativo)**:
- Si eseguono i test sugli stessi dati e hardware
- Si riportano i grafici comparativi
- Si analizzano facilità d’uso, accuratezza, performance.

---

## 📌 Come eseguire

**MATLAB**
```matlab
% Eseguire in MATLAB
run('cholesnki.m')
```
**Python**
```python
python cholesky.py
python comparison_plots.py
```
