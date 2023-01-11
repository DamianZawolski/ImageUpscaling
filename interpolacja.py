import cv2
import numpy as np

def interpolacja_dwuliniowa(lokalizacja):
    zdjecie = cv2.imread(lokalizacja)
    wymiary = (zdjecie.shape[0]*2, zdjecie.shape[1]*2)

    wysokosc = zdjecie.shape[0]
    szerokosc = zdjecie.shape[1]

    skala_x = (szerokosc)/(wymiary[1])
    skala_y = (wysokosc)/(wymiary[0])

    zdjecie_po_interpolacji = np.zeros((wymiary[0], wymiary[1], zdjecie.shape[2]))

    for k in range(3):
        for i in range(wymiary[0]):
            for j in range(wymiary[1]):
                x = (j+0.5) * (skala_x) - 0.5
                y = (i+0.5) * (skala_y) - 0.5
                x_int = min(int(x), szerokosc-2)
                y_int = min(int(y), wysokosc-2)
                x_roznica = x - x_int
                y_roznica = y - y_int
                a = zdjecie[y_int, x_int, k]
                b = zdjecie[y_int, x_int + 1, k]
                c = zdjecie[y_int + 1, x_int, k]
                d = zdjecie[y_int + 1, x_int + 1, k]
                piksel = a*(1-x_roznica)*(1-y_roznica) + b*(x_roznica) * \
                    (1-y_roznica) + c*(1-x_roznica) * (y_roznica) + d*x_roznica*y_roznica

                zdjecie_po_interpolacji[i, j, k] = piksel.astype(np.uint8)

    return zdjecie_po_interpolacji


