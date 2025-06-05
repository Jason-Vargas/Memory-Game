import tkinter as tk
from ventanajuego import VentanaJuego
from interfaz import *

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Memory Game")
        self.ventana.geometry("1200x700")
        self.inicializar_componentes()

    def inicializar_componentes(self):
        etiqueta = tk.Label(self.ventana, text="Memory Game", font=("Arial", 14))
        etiqueta.pack(pady=20)

        boton_jugar = tk.Button(self.ventana, text="Modo Clásico", font=("Arial", 12), command=self.abrir_juego)
        boton_jugar.pack(pady=10)

    def abrir_juego(self):
        self.ventana.withdraw()
        VentanaJuego(self.ventana)

    def ejecutar(self):
        self.ventana.mainloop()

# Ejecutar solo si este archivo es el principal
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.ejecutar()