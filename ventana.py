import tkinter as tk
from PIL import Image, ImageTk
from ventanajuego import VentanaJuego
from interfaz import *

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Memory Game")
        self.ventana.geometry("1200x700")

        self.imagen_fondo = Image.open("IMG//First//Memory.png")
        self.imagen_fondo = self.imagen_fondo.resize((1200, 700))
        self.imagen_fondo_tk = ImageTk.PhotoImage(self.imagen_fondo)

        self.canvas = tk.Canvas(self.ventana, width=1200, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.imagen_fondo_tk, anchor="nw")

        self.inicializar_componentes()

    def inicializar_componentes(self):
        boton_jugar = tk.Button(self.ventana, text="Modo Clásico", font=("Arial", 14), command=self.abrir_juego, bg="gray")

        
        self.canvas.create_window(600, 325, window=boton_jugar)

    def abrir_juego(self):
        self.ventana.withdraw()
        VentanaJuego(self.ventana)

    def ejecutar(self):
        self.ventana.mainloop()