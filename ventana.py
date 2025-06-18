import tkinter as tk
from PIL import Image, ImageTk
from ventanajuego import VentanaJuego  # Ajusta si está en otro lugar
from tkinter import messagebox
import threading
from interfaz import PatternGameGUI  # Suponiendo que el segundo código está en patterngamegui.py
from APIBCCR import TipoCambioBCCR

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
        boton_bot = tk.Button(self.ventana, text="Modo Clásico (Contra Bot)", font=("Arial", 14), 
                            command=self.abrir_juego_bot, bg="gray")
        boton_online = tk.Button(self.ventana, text="Buscar Partida Online", font=("Arial", 14), 
                            command=self.abrir_juego_online, bg="gray")

        boton_patrones = tk.Button(self.ventana, text="Juego de Patrones", font=("Arial", 14), 
                                    command=self.abrir_juego_patrones, bg="gray")

        self.canvas.create_window(600, 300, window=boton_bot)
        self.canvas.create_window(600, 380, window=boton_online)
        self.canvas.create_window(600, 460, window=boton_patrones)

    def abrir_juego_bot(self):
        self.ventana.withdraw()
        juego = VentanaJuego(self.ventana)
        juego.ventana.mainloop()

    def abrir_juego_online(self):
        self.ventana.withdraw()
        respuesta = messagebox.askyesno("Modo Online", "¿Quieres ser servidor?\n(Sí = servidor, No = cliente)")
        juego = VentanaJuego(self.ventana, modo='online', es_servidor=respuesta)
        juego.ventana.mainloop()

    def abrir_juego_patrones(self):
        # Para abrir el juego de patrones sin bloquear esta ventana principal,
        # lo ejecutamos en un hilo separado para no bloquear el hilo principal Tkinter.
        def run_pattern_game():
            app = PatternGameGUI()
            app.run()
        
        threading.Thread(target=run_pattern_game, daemon=True).start()

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.ejecutar()