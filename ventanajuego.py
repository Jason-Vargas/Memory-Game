import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class VentanaJuego:
    def __init__(self, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.ventana = tk.Toplevel()
        self.ventana.title("Juego de Memoria")
        self.ventana.geometry("700x780")
        self.ventana.configure(bg="#f3f3f3")

        self.filas = 6
        self.columnas = 6
        self.boton_size = 90

        self.botones = []
        self.celdas_reveladas = []
        self.imagenes_por_celda = []
        self.total_parejas = (self.filas * self.columnas) // 2
        self.parejas_encontradas = 0

        self.cargar_imagenes()
        self.asignar_imagenes()
        self.crear_interfaz()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cargar_imagenes(self):
        ruta_img = "IMG"
        nombres_png = [nombre for nombre in os.listdir(ruta_img) if nombre.endswith(".png")]
        nombres_png = nombres_png[:self.total_parejas]  # Asegura que no haya más de 18

        self.imagenes_temp = []
        for nombre in nombres_png:
            ruta = os.path.join(ruta_img, nombre)
            imagen = Image.open(ruta).resize((self.boton_size, self.boton_size))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagenes_temp.append(imagen_tk)
            self.imagenes_temp.append(imagen_tk)  # Duplicar para hacer pareja

        random.shuffle(self.imagenes_temp)

    def asignar_imagenes(self):
        self.imagenes_por_celda = []
        idx = 0
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(self.imagenes_temp[idx])
                idx += 1
            self.imagenes_por_celda.append(fila)

    def crear_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana, bg="#f3f3f3")
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame_principal, height=50, bg="#858386")
        self.frame_info.pack(side="top", fill="x")

        

        self.frame_matriz = tk.Frame(self.frame_principal, bg="#696969")
        self.frame_matriz.pack(expand=True, pady=(10, 20))

        self.crear_matriz()

    def crear_matriz(self):
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                frame_celda = tk.Frame(self.frame_matriz, width=self.boton_size, height=self.boton_size, bg="#f3f3f3")
                frame_celda.grid(row=i, column=j, padx=6, pady=6)
                frame_celda.propagate(False)

                boton = tk.Button(frame_celda,
                        bg="#ffffff",
                        relief="flat",
                        bd=0,
                        highlightthickness=0,
                        activebackground="#e6e6e6",
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
            self.ventana.after(800, self.verificar_coincidencia)

    def verificar_coincidencia(self):
        (f1, c1), (f2, c2) = self.celdas_reveladas
        img1 = self.imagenes_por_celda[f1][c1]
        img2 = self.imagenes_por_celda[f2][c2]

        if img1 == img2:
            self.botones[f1][c1].config(state="disabled")
            self.botones[f2][c2].config(state="disabled")
            self.parejas_encontradas += 1

            if self.parejas_encontradas == self.total_parejas:
                messagebox.showinfo("¡Felicidades!", "¡Has encontrado todas las parejas!")
        else:
            self.botones[f1][c1].config(image='')
            self.botones[f2][c2].config(image='')

        self.celdas_reveladas.clear()

    def cerrar_ventana(self):
        self.ventana.destroy()
        self.ventana_anterior.deiconify()