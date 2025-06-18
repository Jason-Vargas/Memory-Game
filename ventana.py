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

    def mostrar_mejores_resultados(self):
        try:
            with open("mejores_resultados.txt", "r") as f:
                lineas = f.readlines()
        except FileNotFoundError:
            lineas = []

        ventana_resultados = tk.Toplevel(self.ventana)
        ventana_resultados.title("🏆 Mejores Resultados")
        ventana_resultados.geometry("400x300")
        ventana_resultados.configure(bg="white")

        titulo = tk.Label(ventana_resultados, text="Top 5 Mejores Resultados", font=("Arial", 16, "bold"), bg="white")
        titulo.pack(pady=10)

        if not lineas:
            tk.Label(ventana_resultados, text="No hay resultados guardados.", font=("Arial", 12), bg="white").pack(pady=10)
        else:
            for linea in lineas:
                tk.Label(ventana_resultados, text=linea.strip(), font=("Arial", 12), bg="white").pack(anchor="w", padx=20)
        
        boton_cerrar = tk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy, bg="lightgray")
        boton_cerrar.pack(pady=15)
    
    def inicializar_componentes(self):
        boton_bot = tk.Button(self.ventana, text="Modo Clásico (Contra Bot)", font=("Arial", 14), 
                            command=self.abrir_juego_bot, bg="gray")
        boton_online = tk.Button(self.ventana, text="Buscar Partida Online", font=("Arial", 14), 
                                command=self.abrir_juego_online, bg="gray")
        boton_patrones = tk.Button(self.ventana, text="Juego de Patrones", font=("Arial", 14), 
                                command=self.abrir_juego_patrones, bg="gray")
        boton_mejores = tk.Button(self.ventana, text="🏅 Ver Mejores Resultados", font=("Arial", 14),
                                command=self.mostrar_mejores_resultados, bg="gold")

        self.canvas.create_window(600, 300, window=boton_bot)
        self.canvas.create_window(600, 380, window=boton_online)
        self.canvas.create_window(600, 460, window=boton_patrones)
        self.canvas.create_window(600, 540, window=boton_mejores)
    
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