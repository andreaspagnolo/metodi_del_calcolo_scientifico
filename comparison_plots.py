import matplotlib.pyplot as plt
import numpy as np

# Dati
windows_data = {
    "Matrix": ["FIDAP/ex15", "MaxPlanck/shallow water1", "Rothberg/cfd1", "Rothberg/cfd2", 
               "Missgott/parabolic_fem", "GHS_psdef/apache2", "AWD/G3_circuit", "Janna/Stocf-1465"],
    "Time_s": [0.012166, 0.14099, 0.87437, 1.5484, 1.2263, 4.1948, 5.9447, 124.66],
    "Memory_MB": [0.052391, 0.625, 0.53906, 0.94177, 4.0117, 5.4564, 12.096, 11.178],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6023e-14, 4.3156e-13, 1.0479e-12, 4.3914e-11, 3.5757e-12, 2.1391e-10]
}

linux_data = {
    "Matrix": ["FIDAP/ext5", "MaxPlanck/shallow_material", "Rothberg/cfdi", "Rothberg/cfd2",
               "Missgott/parabolic_fem", "RMS_pest/Pagache2", "AVO/GS_circuit", "Janna/StoCF-1465"],
    "Time_s": [0.911945, 0.16789, 0.76054, 1.6237, 1.2802, 4.2482, 6.0876, 118.97],
    "Memory_MB": [0.652391, 9.625, 9.53906, 9.94177, 4.0517, 5.4564, 12.896, 11.178],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6923e-14, 4.3156e-13, 1.0978e-12, 4.3914e-11, 3.5757e-12, 1.1825e-10]
}

#Grafico del tempo di esecuzione e dell'errore relativo
x = np.arange(1, len(windows_data["Matrix"]) + 1)
plt.figure(figsize=(12, 6))
plt.plot(x, windows_data["Time_s"], '-o', linewidth=2, color=[0.2, 0.4, 0.8], label='Windows')
plt.plot(x, linux_data["Time_s"], '-o', linewidth=2, color=[0, 0.6, 0], label='Linux')
# Etichette asse X corrette
plt.xticks(x, windows_data["Matrix"], rotation=45)
plt.ylabel("Tempo (s)")
plt.xlabel("Matrice")
plt.title("Tempo di esecuzione per ciascuna matrice (Windows vs Linux)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#Grafico della memoria utilizzata
plt.figure(figsize=(12, 6))
plt.plot(x, windows_data["Memory_MB"], '-o', linewidth=2, color=[0.8, 0.4, 0.2], label='Windows')
plt.plot(x, linux_data["Memory_MB"], '-o', linewidth=2, color=[0, 0.6, 0], label='Linux')
plt.xticks(x, windows_data["Matrix"], rotation=45)
plt.ylabel("Memoria (MB)")
plt.xlabel("Matrice")
plt.title("Uso di memoria per ciascuna matrice (Windows vs Linux)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#Grafico dell'errore relativo
plt.figure(figsize=(12, 6))
plt.plot(x, windows_data["Relative_Error"], '-o', linewidth=2, color=[0.4, 0.2, 0.8], label='Windows')
plt.plot(x, linux_data["Relative_Error"], '-o', linewidth=2, color=[0, 0.6, 0], label='Linux')
plt.xticks(x, windows_data["Matrix"], rotation=45)
plt.ylabel("Errore relativo")
plt.xlabel("Matrice")
plt.title("Errore relativo per ciascuna matrice (Windows vs Linux)")
plt.grid(True)
plt.legend()
plt.yscale('log')  # Errore relativo spesso va su scala logaritmica per essere leggibile
plt.tight_layout()
plt.show()

