import socket
import threading
import tkinter as tk
from tkinter import messagebox

class ClienteJuego:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ventana = tk.Tk()
        self.ventana.title("Juego de Memoria - Cliente")
        self.ventana.geometry("400x300")

        self.texto_estado = tk.StringVar()
        self.texto_estado.set("Conectando al servidor...")
        self.label_estado = tk.Label(self.ventana, textvariable=self.texto_estado)
        self.label_estado.pack(pady=20)

        self.boton_turno = tk.Button(self.ventana, text="Simular Movimiento", command=self.enviar_movimiento, state="disabled")
        self.boton_turno.pack(pady=10)

        self.conectar()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.ventana.mainloop()

    def conectar(self):
        try:
            self.socket.connect((self.host, self.puerto))
            self.texto_estado.set("Conectado al servidor. Esperando turno...")
            threading.Thread(target=self.recibir_datos, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")
            self.ventana.destroy()

    def recibir_datos(self):
        while True:
            try:
                datos = self.socket.recv(1024).decode()
                if datos == "TURNO":
                    self.texto_estado.set("Es tu turno")
                    self.boton_turno.config(state="normal")
                elif datos.startswith("MOVIMIENTO"):
                    movimiento = datos.split(":")[1]
                    self.texto_estado.set(f"Otro jugador movió: {movimiento}")
                elif datos == "FIN":
                    self.texto_estado.set("Juego terminado")
                    break
            except:
                break

    def enviar_movimiento(self):
        self.socket.sendall(b"MOVIMIENTO:Revelo una carta")
        self.boton_turno.config(state="disabled")
        self.texto_estado.set("Esperando al otro jugador...")

    def cerrar(self):
        try:
            self.socket.close()
        except:
            pass
        self.ventana.destroy()


class ServidorJuego:
    def __init__(self, puerto):
        self.puerto = puerto
        self.clientes = []
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(("", self.puerto))
        self.servidor.listen(2)
        print(f"Servidor iniciado en el puerto {self.puerto}. Esperando jugadores...")

        threading.Thread(target=self.aceptar_clientes, daemon=True).start()

    def aceptar_clientes(self):
        while len(self.clientes) < 2:
            cliente, _ = self.servidor.accept()
            self.clientes.append(cliente)
            print("Jugador conectado")

        # Iniciar juego cuando haya 2 jugadores
        self.juego()

    def juego(self):
        turno = 0
        while True:
            cliente_actual = self.clientes[turno]
            cliente_oponente = self.clientes[1 - turno]

            try:
                cliente_actual.sendall(b"TURNO")
                datos = cliente_actual.recv(1024)
                if not datos:
                    break
                cliente_oponente.sendall(b"MOVIMIENTO:" + datos.split(b":")[1])
            except:
                break

            turno = 1 - turno

        for c in self.clientes:
            try:
                c.sendall(b"FIN")
                c.close()
            except:
                pass
        self.servidor.close()


# Para probar el servidor, descomenta esto y ejecútalo en un archivo separado
# servidor = ServidorJuego(5000)

# Para probar el cliente, descomenta esto y ejecútalo en otro archivo diferente
# cliente = ClienteJuego("localhost", 5000)
