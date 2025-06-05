import tkinter as tk
from PIL import Image, ImageTk

import tkinter as tk
from PIL import Image, ImageTk
import random
import os

import tkinter as tk
from PIL import Image, ImageTk
import random
import os

class VentanaJuego:
    def __init__(self, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.ventana = tk.Toplevel()
        self.ventana.title("Juego de Memoria")
        self.ventana.geometry("600x600")
        self.filas = 4
        self.columnas = 4
        self.boton_size = 90

        self.botones = []
        self.celdas_reveladas = []
        self.imagenes_por_celda = []

        self.nombres_imagenes = ["Bird", "Block", "Ghost", "Heart", "Monkey", "Nave", "Shield", "Timer"]
        self.cargar_imagenes()
        self.asignar_imagenes()
        self.crear_interfaz()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cargar_imagenes(self):
        ruta_img = "IMG"
        imagenes_temp = []

        for nombre in self.nombres_imagenes:
            ruta = os.path.join(ruta_img, nombre + ".png")
            imagen = Image.open(ruta).resize((self.boton_size, self.boton_size))
            imagen_tk = ImageTk.PhotoImage(imagen)
            imagenes_temp.append(imagen_tk)
            imagenes_temp.append(imagen_tk)  # duplicar para la pareja

        random.shuffle(imagenes_temp)
        self.imagenes_asignadas = imagenes_temp

    def asignar_imagenes(self):
        self.imagenes_por_celda = []
        idx = 0
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(self.imagenes_asignadas[idx])
                idx += 1
            self.imagenes_por_celda.append(fila)

    def crear_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame_principal, height=40, bg="lightgray")
        self.frame_info.pack(side="top", fill="x")
        etiqueta_info = tk.Label(self.frame_info, text="Jason Vargas", font=("Arial", 14))
        etiqueta_info.pack(expand=True)

        self.frame_matriz = tk.Frame(self.frame_principal)
        self.frame_matriz.pack(expand=True, pady=(10, 20))

        self.crear_matriz()

    def crear_matriz(self):
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                frame_celda = tk.Frame(self.frame_matriz, width=self.boton_size, height=self.boton_size)
                frame_celda.grid(row=i, column=j, padx=5, pady=5)
                frame_celda.propagate(False)

                boton = tk.Button(frame_celda,
                        bg="white",
                        relief="raised",
                        command=lambda f=i, c=j: self.revelar_imagen(f, c))
                boton.pack(fill="both", expand=True)
                fila.append(boton)
            self.botones.append(fila)

    def revelar_imagen(self, fila, col):
        if len(self.celdas_reveladas) >= 2:
            return

        boton = self.botones[fila][col]
        if boton["state"] == "disabled" or (fila, col) in self.celdas_reveladas:
            return

        imagen = self.imagenes_por_celda[fila][col]
        boton.config(image=imagen)
        self.celdas_reveladas.append((fila, col))

        if len(self.celdas_reveladas) == 2:
            self.ventana.after(1000, self.verificar_coincidencia)

    def verificar_coincidencia(self):
        (f1, c1), (f2, c2) = self.celdas_reveladas
        img1 = self.imagenes_por_celda[f1][c1]
        img2 = self.imagenes_por_celda[f2][c2]

        if img1 == img2:
            self.botones[f1][c1].config(state="disabled")
            self.botones[f2][c2].config(state="disabled")
        else:
            self.botones[f1][c1].config(image='')
            self.botones[f2][c2].config(image='')

        self.celdas_reveladas.clear()

    def cerrar_ventana(self):
        self.ventana.destroy()
        self.ventana_anterior.deiconify()