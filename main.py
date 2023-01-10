import cv2
import os
import PySimpleGUI as sg
import numpy as np

def filtr_splotowy(zdjecie, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    x_kernel = kernel.shape[0]
    y_kernel = kernel.shape[1]
    x_zdjecie = zdjecie.shape[0]
    y_zdjecie = zdjecie.shape[1]
    x_wyjscie = int((x_zdjecie - x_kernel) + 1)
    y_wejscie = int((y_zdjecie - y_kernel) + 1)
    wyjscie = np.zeros((x_wyjscie, y_wejscie))

    for y in range(zdjecie.shape[1]):
        if y > zdjecie.shape[1] - y_kernel:
            break
        for x in range(zdjecie.shape[0]):
            if x > zdjecie.shape[0] - x_kernel:
                break
            try:
                wyjscie[x, y] = int((kernel * zdjecie[x: x + x_kernel, y: y + y_kernel]).sum())
            except:
                break

    imin = wyjscie.min()
    imax = wyjscie.max()
    a = (255 - 0) / (imax - imin)
    b = 255 - a * imax
    wyjscie = (a * wyjscie + b).astype(np.uint8)
    return wyjscie

layout = [
    [sg.Image(key="-IMAGE-")],
    [
        sg.Text("Plik ze zdjęciem"),
        sg.Input(size=(25, 1), key="-FILE-"),
        sg.FileBrowse("Wybierz zdjęcie", file_types=[("All files (*.*)", "*.*")]),
        sg.Button("Wyostrz"),
    ],
]

okno = sg.Window("Image Upscaler 260353", layout)

while True:
    zdarzenie, wartosci = okno.read()
    if zdarzenie == "Wyjście" or zdarzenie == sg.WIN_CLOSED:
        break
    if zdarzenie == "Wyostrz":
        nazwa_pliku = wartosci["-FILE-"].split("/")[-1]
        print(f"Wyostrzany plik to: {nazwa_pliku}")
        if os.path.exists(nazwa_pliku):
            zdjecie = cv2.imread(nazwa_pliku)
            zdjecie = cv2.cvtColor(src=zdjecie, code=cv2.COLOR_BGR2GRAY)
            cv2.imshow('Oryginalne zdjecie', zdjecie)

            # Łagodniejsze wyostrzenie
            kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
            # Mocniejsze wyostrzenie
            #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

            wlasna_implementacja = filtr_splotowy(zdjecie, kernel)
            cv2.imwrite('WlasnaImplementacja.png', wlasna_implementacja)
            cv2.imshow('Wlasna implementacja', wlasna_implementacja)

            wyostrzone_cv2 = cv2.filter2D(src=zdjecie, ddepth=-1, kernel=kernel)
            cv2.imwrite("CV2.png", wyostrzone_cv2)
            cv2.imshow('Zdjecie wyostrzone przy pomocy pakietu CV2', wyostrzone_cv2)


            cv2.waitKey()
            cv2.destroyAllWindows()

okno.close()
