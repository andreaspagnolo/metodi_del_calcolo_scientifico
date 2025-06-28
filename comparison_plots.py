import matplotlib.pyplot as plt
import numpy as np

# Dati
windows_data = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465"
    ],
    "Time_s": [0.076166, 0.1605, 0.99327, 1.7152, 1.3306, 4.3139, 5.908, 1388.6],
    "Memory_MB": [0.16819, 1.8859, 1.6172, 2.8253, 12.035, 16.369, 36.289, 33.534],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6023e-14, 4.3156e-13, 1.0479e-12, 4.3914e-11, 3.5757e-12, 2.4346e-10]
}

linux_data = {
    "Matrix": [
        "FIDAP/ex15", "MaxPlanck/shallow_water1", "Rothberg/cfd1", "Rothberg/cfd2",
        "Wissgott/parabolic_fem", "GHS_psdef/apache2", "AMD/G3_circuit", "Janna/StocF-1465"
    ],
    "Time_s": [0.010164, 0.15419, 0.75225, 1.9068, 1.2791, 4.2278, 5.8966, 115.92],
    "Memory_MB": [0.16819, 1.8859, 1.6172, 2.8253, 12.035, 16.369, 36.289, 33.534],
    "Relative_Error": [6.211e-07, 2.3773e-16, 9.6023e-14, 4.3156e-13, 1.0479e-12, 4.3914e-11, 3.5757e-12, 1.1825e-10]
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

