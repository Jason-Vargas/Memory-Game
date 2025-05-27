import tkinter as tk

class MiVentana:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana en POO")
        self.ventana.geometry("1200x700")
        self.inicializar_componentes()

    def inicializar_componentes(self):
        etiqueta = tk.Label(self.ventana, text="¡Hola desde una clase!", font=("Arial", 14))
        etiqueta.pack(pady=20)

    def ejecutar(self):
        self.ventana.mainloop()

# Crear y ejecutar la ventana
if __name__ == "__main__":
    app = MiVentana()
    app.ejecutar()
