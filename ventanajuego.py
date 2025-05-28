import tkinter as tk
from PIL import Image, ImageTk

class VentanaJuego:
    def __init__(self, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.ventana = tk.Toplevel()
        self.ventana.title("Ventana de Juego")
        self.ventana.geometry("600x600")
        self.filas = 6
        self.columnas = 6
        self.boton_size = 90

        imagen = Image.open("IMG/Ball.png").resize((self.boton_size, self.boton_size))
        self.imagen_tk = ImageTk.PhotoImage(imagen)

        self.botones = []

        self.crear_interfaz()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def crear_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana)
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame_principal, height=50, bg="lightgray")
        self.frame_info.pack(side="top", fill="x")
        etiqueta_info = tk.Label(self.frame_info, text="Jason Vargas", font=("Arial", 16))
        etiqueta_info.pack(expand=True)

        self.frame_matriz = tk.Frame(self.frame_principal)
        self.frame_matriz.pack(expand=True, pady=(10, 30))  # espacio arriba y abajo de la matriz

        self.crear_matriz()

    def crear_matriz(self):
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                frame_celda = tk.Frame(self.frame_matriz, width=self.boton_size, height=self.boton_size)
                frame_celda.grid(row=i, column=j, padx=2, pady=2)
                frame_celda.propagate(False)

                boton = tk.Button(frame_celda,
                        bg="white",
                        relief="raised",
                        command=lambda f=i, c=j: self.revelar_imagen(f, c))
                boton.pack(fill="both", expand=True)
                fila.append(boton)
            self.botones.append(fila)

    def revelar_imagen(self, fila, col):
        self.botones[fila][col].config(image=self.imagen_tk, state="disabled")

    def cerrar_ventana(self):
        self.ventana.destroy()
        self.ventana_anterior.deiconify()
