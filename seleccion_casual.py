import tkinter as tk
from tkinter import messagebox
from ventanajuego import VentanaJuego  # Ajusta la importación según tu estructura

class SeleccionJuego:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Seleccionar Modo de Juego")
        self.ventana.geometry("300x150")
        self.ventana.configure(bg="#282c34")

        self.label = tk.Label(self.ventana, text="Selecciona modo de juego", 
                              fg="white", bg="#282c34", font=("Arial", 14))
        self.label.pack(pady=20)

        self.btn_bot = tk.Button(self.ventana, text="Jugar contra Bot", width=20, 
                                 command=self.jugar_bot)
        self.btn_bot.pack(pady=5)

        self.btn_online = tk.Button(self.ventana, text="Buscar partida online", width=20, 
                                    command=self.jugar_online)
        self.btn_online.pack(pady=5)

        self.ventana.mainloop()

    def jugar_bot(self):
        self.ventana.destroy()
        # Aquí lanzás tu juego en modo Bot
        juego = VentanaJuego(None, modo='bot')  
        juego.ventana.mainloop()

    def jugar_online(self):
        self.ventana.destroy()
        respuesta = messagebox.askyesno("Modo Online", "¿Quieres ser servidor?\n(Sí = servidor, No = cliente)")
        if respuesta:
            juego = VentanaJuego(None, modo='online', es_servidor=True)
        else:
            juego = VentanaJuego(None, modo='online', es_servidor=False)
        juego.ventana.mainloop()


if __name__ == "__main__":
    SeleccionJuego()