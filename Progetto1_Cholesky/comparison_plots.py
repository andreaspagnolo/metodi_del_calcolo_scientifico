import matplotlib.pyplot as plt
import numpy as np

# Dati MATLAB
matlab_windows = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465"
    ],
    "Time_s": [0.13902, 0.1443, 0.85977, 1.8995, 1.2987, 4.8637, 7.0524, 1399.1],
    "Memory_MB": [0.16958, 1.89, 1.6172, 2.8253, 12.035, 16.369, 36.289, 33.534],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6023e-14, 4.3156e-13, 1.0479e-12, 4.3914e-11, 3.5757e-12, 2.4346e-10]
}

matlab_linux = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465"
    ],
    "Time_s": [0.3714, 0.17019, 0.7074, 1.5487, 1.2249, 4.2136, 5.9785, 116.62],
    "Memory_MB": [0.16958, 1.89, 1.6172, 2.8253, 12.035, 16.369, 36.289, 33.534],
    "Memory_Peak_MB": [1288.7, 1346, 1769.4, 2243.6, 2243.6, 3487.4, 3960.8, 12096],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6023e-14, 4.3156e-13, 1.0479e-12, 4.3914e-11, 3.5757e-12, 1.1825e-10]
}

# Dati Python
python_windows = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465", "Janna/Flan_1565"
    ],
    "Time_s": [2.5923e-02, 5.3437e-01, 3.6364, 9.9077, 5.4470, 56.655, 23.668, 1259.8, 1362.2],
    "Memory_MB": [4.30, 6.46, 28.26, 42.71, 85.23, 100.58, 193.09, 320.08, -64.25],
    "MemoryPeak_MB": [108.08, 69.43, 327.56, 526.85, 517.29, 1517.35, 1259.42, 9852.42, 12907.82],
    "Relative_Error": [6.37e-07, 2.42e-16, 5.73e-14, 2.53e-13, 1.22e-12, 2.74e-11, 2.74e-12, 3.64e-10, 6.81e-11]
}

python_linux = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465"
    ],
    "Time_s": [8.1356e-02, 2.0184e-01, 1.5211, 2.6874, 2.0305, 11.905, 14.617, 86.938],
    "Memory_MB": [5.46, 12.02, 112.51, -19.89, 91.78, 32.15, 112.70, 382.55],
    "MemoryPeak_MB": [82.22, 132.26, 378.37, 899.42, 613.29, 1806.17, 1553.34, 10422.96],
    "Relative_Error": [5.81e-07, 2.02e-16, 6.60e-14, 2.71e-13, 7.06e-13, 3.54e-11, 3.92e-12, 3.69e-10]
}

# Preparazione dei dati per il plotting
matrix_names = matlab_windows["Matrix"]  # Matrici comuni a tutti i dataset
x = np.arange(len(matrix_names))

# Stile uniforme per tutti i grafici
line_style = {
    'MATLAB Windows': {'color': 'royalblue', 'marker': 'o', 'linestyle': '-', 'linewidth': 2},
    'MATLAB Linux': {'color': 'lightblue', 'marker': 's', 'linestyle': '--', 'linewidth': 2},
    'Python Windows': {'color': 'darkgreen', 'marker': 'o', 'linestyle': '-', 'linewidth': 2},
    'Python Linux': {'color': 'lightgreen', 'marker': 's', 'linestyle': '--', 'linewidth': 2}
}

# Estrai i dati per le matrici comuni
matlab_win_times = matlab_windows["Time_s"]
matlab_lin_times = [matlab_linux["Time_s"][matlab_linux["Matrix"].index(m)] for m in matrix_names]
python_win_times = [python_windows["Time_s"][python_windows["Matrix"].index(m)] if m in python_windows["Matrix"] else np.nan for m in matrix_names]
python_lin_times = [python_linux["Time_s"][python_linux["Matrix"].index(m)] if m in python_linux["Matrix"] else np.nan for m in matrix_names]

# 1. Grafico tempi di esecuzione con griglia semplificata
plt.figure(figsize=(14, 7))

plt.plot(x, matlab_win_times, label='MATLAB Windows', **line_style['MATLAB Windows'])
plt.plot(x, matlab_lin_times, label='MATLAB Linux', **line_style['MATLAB Linux'])
plt.plot(x, python_win_times, label='Python Windows', **line_style['Python Windows'])
plt.plot(x, python_lin_times, label='Python Linux', **line_style['Python Linux'])
plt.xticks(x, matrix_names, rotation=45, ha='right')
plt.ylabel('Tempo (s)')
plt.xlabel('Matrice')
plt.title('Confronto tempi di esecuzione')
plt.yscale('log')
plt.grid(True, which='major', ls='--', alpha=0.7)
plt.grid(False, which='minor')  # Disabilitiamo la griglia minore
plt.legend()
plt.tight_layout()
plt.show()

# 2. Grafico uso memoria (stile lineare)
plt.figure(figsize=(14, 7))

# Filtra valori negativi e prepara dati
matlab_win_mem = [max(0, m) for m in matlab_windows["Memory_MB"]]
matlab_lin_mem = [max(0, matlab_linux["Memory_MB"][matlab_linux["Matrix"].index(m)]) for m in matrix_names]
python_win_mem = [max(0, python_windows["Memory_MB"][python_windows["Matrix"].index(m)]) if m in python_windows["Matrix"] else np.nan for m in matrix_names]
python_lin_mem = [max(0, python_linux["Memory_MB"][python_linux["Matrix"].index(m)]) if m in python_linux["Matrix"] else np.nan for m in matrix_names]

plt.plot(x, matlab_win_mem, label='MATLAB Windows', **line_style['MATLAB Windows'])
plt.plot(x, matlab_lin_mem, label='MATLAB Linux', **line_style['MATLAB Linux'])
plt.plot(x, python_win_mem, label='Python Windows', **line_style['Python Windows'])
plt.plot(x, python_lin_mem, label='Python Linux', **line_style['Python Linux'])

plt.xticks(x, matrix_names, rotation=45, ha='right')
plt.ylabel('Memoria utilizzata (MB)')
plt.xlabel('Matrice')
plt.title('Confronto uso memoria (stile lineare)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()

# 3. Grafico errore relativo (come nel tuo esempio originale)
plt.figure(figsize=(14, 7))

matlab_win_err = matlab_windows["Relative_Error"]
matlab_lin_err = [matlab_linux["Relative_Error"][matlab_linux["Matrix"].index(m)] for m in matrix_names]
python_win_err = [python_windows["Relative_Error"][python_windows["Matrix"].index(m)] if m in python_windows["Matrix"] else np.nan for m in matrix_names]
python_lin_err = [python_linux["Relative_Error"][python_linux["Matrix"].index(m)] if m in python_linux["Matrix"] else np.nan for m in matrix_names]

plt.plot(x, matlab_win_err, label='MATLAB Windows', **line_style['MATLAB Windows'])
plt.plot(x, matlab_lin_err, label='MATLAB Linux', **line_style['MATLAB Linux'])
plt.plot(x, python_win_err, label='Python Windows', **line_style['Python Windows'])
plt.plot(x, python_lin_err, label='Python Linux', **line_style['Python Linux'])

plt.xticks(x, matrix_names, rotation=45, ha='right')
plt.ylabel('Errore relativo')
plt.xlabel('Matrice')
plt.title('Confronto precisione numerica (stile lineare)')
plt.yscale('log')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()

# 4. Grafico memoria di picco (stile lineare)
plt.figure(figsize=(14, 7))

# Solo per MATLAB Linux e Python
matlab_lin_peak = [matlab_linux["Memory_Peak_MB"][matlab_linux["Matrix"].index(m)] for m in matrix_names]
python_win_peak = [python_windows["MemoryPeak_MB"][python_windows["Matrix"].index(m)] if m in python_windows["Matrix"] else np.nan for m in matrix_names]
python_lin_peak = [python_linux["MemoryPeak_MB"][python_linux["Matrix"].index(m)] if m in python_linux["Matrix"] else np.nan for m in matrix_names]

plt.plot(x, matlab_lin_peak, label='MATLAB Linux', **line_style['MATLAB Linux'])
plt.plot(x, python_win_peak, label='Python Windows', **line_style['Python Windows'])
plt.plot(x, python_lin_peak, label='Python Linux', **line_style['Python Linux'])

plt.xticks(x, matrix_names, rotation=45, ha='right')
plt.ylabel('Memoria di picco (MB)')
plt.xlabel('Matrice')
plt.title('Confronto memoria di picco (stile lineare)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()
