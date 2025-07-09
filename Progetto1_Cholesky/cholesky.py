import os
import numpy as np
import scipy.io
import scipy.sparse
from sksparse.cholmod import cholesky
import time
import psutil
import tracemalloc
#from memory_profiler import memory_usage
from matplotlib import pyplot as plt

def solve_with_cholesky(A, b):
    factor = cholesky(A)
    return factor(b)

def solve_sparse_cholesky(mat_file):

    process = psutil.Process(os.getpid())
    before = process.memory_info().rss
    tracemalloc.start()

    # Carica la matrice dal file .mat
    mat = scipy.io.loadmat(mat_file)
    A = scipy.sparse.csc_matrix(mat['Problem']['A'][0][0])

    # Rimozione entry nulle
    A.eliminate_zeros()

    # Controllo di simmetria
    if A.shape[0] != A.shape[1]:
        print("Attenzione: La matrice non è simmetrica")
        return False
    
    diff = A - A.T
    max_diff = np.max(np.abs(diff.data)) if diff.nnz > 0 else 0.0
    if max_diff > 1e-10:
        print("Attenzione: La matrice non è simmetrica")
        return False

    # # Controllo se definita positiva
    # vals = scipy.sparse.linalg.eigsh(A, k=6, return_eigenvectors=False, which='SM')
    # if np.any(vals <= 0):
    #     print("Attenzione: La matrice ha autovalori non positivi")
    #     return False

    print('Finiti i controlli...')
    
    

    n = A.shape[0]

    # Costruisce la soluzione per il calcolo dell'errore
    xe = np.ones(n)
    b = A * xe

    
    # Calcolo tempo per la soluzione
    start_time = time.time()
    #mem_usage, x = memory_usage((solve_with_cholesky, (A, b)), retval=True, max_usage=True)

    x = solve_with_cholesky(A,b)
    
    end_time = time.time()

    after = process.memory_info().rss
    delta = (after - before) / 1024**2 # in MB

    # Metriche
    time_elapsed = end_time - start_time
    rel_error = np.linalg.norm(x - xe) / np.linalg.norm(xe)
    mem_used = delta  

    return {
        'matrix': os.path.basename(mat_file),
        'size': n,
        'time': time_elapsed,
        'error': rel_error,
        'memory': mem_used
    }

def plot_results(results):
    
    sizes = [r['size'] for r in results]
    times = [r['time'] for r in results]
    errors = [r['error'] for r in results]
    memories = [r['memory'] for r in results]

    # Grafico 1: Tempo
    plt.figure(figsize=(8, 6))
    plt.semilogy(sizes, times, 'o-', color='blue', label='Tempo (s)')
    plt.title('Tempo in funzione della dimensione matrice')
    plt.xlabel('Dimensione matrice')
    plt.ylabel('Tempo (s)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Grafico 2: Errore relativo
    plt.figure(figsize=(8, 6))
    plt.semilogy(sizes, errors, 's-', color='green', label='Errore relativo')
    plt.title('Errore relativo in funzione della dimensione matrice')
    plt.xlabel('Dimensione matrice')
    plt.ylabel('Errore relativo')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Grafico 3: Memoria
    plt.figure(figsize=(8, 6))
    plt.semilogy(sizes, memories, '^-', color='red', label='Memoria (MB)')
    plt.title('Memoria in funzione della dimensione matrice')
    plt.xlabel('Dimensione matrice')
    plt.ylabel('Memoria (MB)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Grafico complessivo
    plt.figure(figsize=(8, 6))
    
    plt.semilogy(sizes, times, 'o-', label='Tempo (s)')
    plt.semilogy(sizes, errors, 's-', label='Errore relativo')
    plt.semilogy(sizes, memories, '^-', label='Memoria (MB)')

    plt.title('Prestazioni in funzione della dimensione matrice')
    plt.xlabel('Dimensione matrice')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    
    matrices_folder_path = 'data'
    results = []
    for matrix_name in os.listdir(matrices_folder_path):
        
        if matrix_name.endswith(".mat"): 
            print('Risolvendo la matrice:', matrix_name)
            res = solve_sparse_cholesky(os.path.join(matrices_folder_path, matrix_name))
            results.append(res)
            print(res)
    
    results = sorted(results, key=lambda x: x["size"])

    print(" --- Risultati delle simulazioni ---")

    # Print header
    print(f"{'Matrix':>24} | {'Size':>10} | {'Time (s)':>10} | {'Rel. Error':>12} | {'Memory (MB)':>13}")
    print('-' * 80)
    
    # Print rows
    for r in results:
        print(f"{r['matrix']:>24} | {r['size']:>10.4e} | {r['time']:>10.4e} | {r['error']:>12.2e} | {r['memory']:>13.2f}")  
        


    plot_results(results)

    plot_results(results)
