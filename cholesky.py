
import os
import numpy as np
import scipy.io
import scipy.sparse
from sksparse.cholmod import cholesky
import time
from memory_profiler import memory_usage
from matplotlib import pyplot as plt

def solve_with_cholesky(A, b):
    factor = cholesky(A)
    return factor(b)

def solve_sparse_cholesky(mat_file):
    # Carica la matrice dal file .mat
    mat = scipy.io.loadmat(mat_file, spmatrix=True)
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

    # Costruisce xe = [1, 1, ..., 1] e b = A @ xe
    xe = np.ones(n)
    b = A * xe

    # Tempo e memoria usata per la soluzione
    start_time = time.time()
    mem_usage, x = memory_usage((solve_with_cholesky, (A, b)), retval=True, max_usage=True)
    end_time = time.time()

    # Metriche
    time_elapsed = end_time - start_time
    rel_error = np.linalg.norm(x - xe) / np.linalg.norm(xe)
    mem_used = mem_usage  # in MB

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

    plt.figure(figsize=(8, 6))
    
    plt.semilogy(sizes, times, 'o-', label='Tempo (s)')
    plt.semilogy(sizes, errors, 's-', label='Errore relativo')
    plt.semilogy(sizes, memories, '^-', label='Memoria (MB)')

    plt.yscale('log')
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
    print(f"{'Matrix':>12} | {'Time (s)':>10} | {'Rel. Error':>12} | {'Memory (MB)':>13}")
    print('-' * 56)
    
    # Print rows
    for r in results:
        print(f"{r['matrix']:>12} | {r['time']:>10.4e} | {r['error']:>12.2e} | {r['memory']:>13.2f}")


    plot_results(results)

