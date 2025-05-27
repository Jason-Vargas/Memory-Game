import tkinter as tk

class VentanaJuego:
    def __init__(self, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.ventana = tk.Toplevel()
        self.ventana.title("Ventana de Juego")
        self.ventana.geometry("600x600")
        self.crear_matriz(6, 6)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def crear_matriz(self, filas, columnas):
        for i in range(filas):
            for j in range(columnas):
                boton = tk.Button(self.ventana, text=f"{i},{j}", width=10, height=4)
                boton.grid(row=i, column=j, padx=2, pady=2)

    def cerrar_ventana(self):
        self.ventana.destroy()
        self.ventana_anterior.deiconify()

