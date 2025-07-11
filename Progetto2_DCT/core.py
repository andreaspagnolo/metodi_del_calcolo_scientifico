import numpy as np
from scipy.fftpack import dctn, idctn

def dct2(block):
    return dctn(block, type=2, norm='ortho')

def idct2(block):
    return idctn(block, type=2, norm='ortho')

def compress_image(image, F, d):
    arr = np.array(image, dtype=np.float64)
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

    return arr_comp.astype(np.uint8)
