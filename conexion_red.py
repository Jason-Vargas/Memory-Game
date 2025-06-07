import socket
import threading
import pickle

class ConexionRed:
    def __init__(self, es_servidor, host='localhost', puerto=5000):
        self.es_servidor = es_servidor
        self.host = host
        self.puerto = puerto
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion = None
        self.escuchando = False
        self.callback_recepcion = None

    def iniciar(self):
        if self.es_servidor:
            self.socket.bind((self.host, self.puerto))
            self.socket.listen(1)
            print("Esperando conexión...")
            self.conexion, _ = self.socket.accept()
            print("Cliente conectado.")
        else:
            self.socket.connect((self.host, self.puerto))
            self.conexion = self.socket
            print("Conectado al servidor.")

        self.escuchando = True
        threading.Thread(target=self.escuchar, daemon=True).start()

    def escuchar(self):
        while self.escuchando:
            try:
                datos = self.conexion.recv(4096)
                if datos:
                    mensaje = pickle.loads(datos)
                    if self.callback_recepcion:
                        self.callback_recepcion(mensaje)
            except:
                break

    def enviar(self, mensaje):
        try:
            datos = pickle.dumps(mensaje)
            self.conexion.sendall(datos)
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

    def cerrar(self):
        self.escuchando = False
        try:
            self.socket.close()
        except:
            pass
