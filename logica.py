import json

class GestorUsuarios:
    ARCHIVO_USUARIOS = "usuarios.json"

    def __init__(self):
        self.usuarios = self.cargar_usuarios()

    def cargar_usuarios(self):
        try:
            with open(self.ARCHIVO_USUARIOS, "r") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return {}

    def guardar_usuarios(self):
        with open(self.ARCHIVO_USUARIOS, "w") as archivo:
            json.dump(self.usuarios, archivo)

    def validar_usuario(self, usuario, contraseña):
        return self.usuarios.get(usuario) == contraseña

    def registrar_usuario(self, usuario, contraseña):
        if usuario in self.usuarios:
            return False  # Usuario ya existe
        
        self.usuarios[usuario] = contraseña
        self.guardar_usuarios()
        return True  # Registro exitoso