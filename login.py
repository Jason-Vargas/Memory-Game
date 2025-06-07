import tkinter as tk
from tkinter import messagebox
from logica import GestorUsuarios  # Importamos la clase lógica
<<<<<<< HEAD

# SOLUCIÓN 1: Importar la clase en lugar de main_gui
try:
    from face_gui import FaceRecognitionGUI  # Importar la clase nueva
except ImportError:
    # Si face_gui todavía tiene la función main_gui, usar esta línea:
    import face_gui
=======
import face_gui  # Importamos el módulo completo
>>>>>>> origin/main

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 ¡Bienvenido! 🎉")
        self.root.geometry("350x400")
        self.root.configure(bg="#3BDBFF")  # Fondo
        
        self.gestor = GestorUsuarios()  # Instancia de la lógica
        
        # Estilos mejorados
        label_fg = "#4A148C"
        label_bg = "#3BC1FF"
        entry_bg = "#FFF"
        button_bg = "#6200EA"
        button_fg = "white"
        button_font = ("Comic Sans MS", 12, "bold")
        
        # Widgets con fuentes y colores divertidos
        tk.Label(self.root, text="👤 Usuario:", fg=label_fg, bg=label_bg, font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_usuario = tk.Entry(self.root, bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_usuario.pack(pady=5)
        
        tk.Label(self.root, text="🔑 Contraseña:", fg=label_fg, bg=label_bg, font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_contraseña = tk.Entry(self.root, show="*", bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_contraseña.pack(pady=5)
        
        tk.Button(self.root, text="🚀 Ingresar", command=self.verificar_login, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
        tk.Button(self.root, text="✨ Registrarse", command=self.registrar_nuevo_usuario, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
<<<<<<< HEAD
        tk.Button(self.root, text="😎 Face ID", command=self.iniciar_sesion_face_id, bg="#27AE60", fg="white", font=button_font).pack(pady=5)
        tk.Button(self.root, text="❌ Salir", bg="#E74C3C", fg="white", font=button_font, command=self.root.quit).pack(pady=5)
=======
        tk.Button(self.root, text="😎 Face ID", command=self.iniciar_sesion_face_id, bg="#27AE60", fg="white", font=button_font).pack(pady=5)  # Botón de Face ID
        tk.Button(self.root, text="❌ Salir", bg="#E74C3C", fg="white", font=button_font, command=self.root.quit).pack(pady=5)  # Botón de salir
>>>>>>> origin/main
    
    def verificar_login(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        if self.gestor.validar_usuario(usuario, contraseña):
            messagebox.showinfo("🎉 Éxito", "¡Login exitoso! 🥳")
        else:
            messagebox.showerror("⚠️ Error", "Usuario o contraseña incorrectos 😕")
    
    def registrar_nuevo_usuario(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        if not usuario or not contraseña:
            messagebox.showwarning("🤔 Advertencia", "Debe ingresar usuario y contraseña")
            return
        
        if self.gestor.registrar_usuario(usuario, contraseña):
            messagebox.showinfo("🎊 Registro", "¡Usuario registrado con éxito! 🎈")
        else:
            messagebox.showerror("😣 Error", "El usuario ya existe")
    
    def iniciar_sesion_face_id(self):
<<<<<<< HEAD
        """Inicia el sistema de reconocimiento facial."""
        try:
            # SOLUCIÓN 1: Si tienes la versión con clases
            if 'FaceRecognitionGUI' in globals():
                face_app = FaceRecognitionGUI()
                face_app.run()
            else:
                # SOLUCIÓN 2: Si tienes la versión original con main_gui
                if hasattr(face_gui, 'main_gui'):
                    face_gui.main_gui()
                elif hasattr(face_gui, 'main'):
                    face_gui.main()
                else:
                    messagebox.showerror("Error", "No se encontró la función de Face ID")
        except Exception as e:
            messagebox.showerror("Error Face ID", f"Error al iniciar Face ID: {str(e)}")


# ALTERNATIVA: Función auxiliar para manejar ambas versiones
def iniciar_face_recognition():
    """Función auxiliar para iniciar el reconocimiento facial."""
    try:
        # Intentar con la nueva versión (clases)
        from face_gui import FaceRecognitionGUI
        app = FaceRecognitionGUI()
        app.run()
    except (ImportError, AttributeError):
        try:
            # Intentar con la versión original
            import face_gui
            if hasattr(face_gui, 'main_gui'):
                face_gui.main_gui()
            elif hasattr(face_gui, 'main'):
                face_gui.main()
            else:
                raise AttributeError("No se encontró función de Face ID")
        except Exception as e:
            messagebox.showerror("Error Face ID", f"Error al iniciar Face ID: {str(e)}")


class LoginAppMejorado:
    """Versión mejorada con mejor manejo de errores."""
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 ¡Bienvenido! 🎉")
        self.root.geometry("350x400")
        self.root.configure(bg="#3BDBFF")
        
        self.gestor = GestorUsuarios()
        self.setup_gui()
    
    def setup_gui(self):
        """Configura la interfaz gráfica."""
        # Estilos
        label_fg = "#4A148C"
        label_bg = "#3BC1FF"
        entry_bg = "#FFF"
        button_bg = "#6200EA"
        button_fg = "white"
        button_font = ("Comic Sans MS", 12, "bold")
        
        # Widgets
        tk.Label(self.root, text="👤 Usuario:", fg=label_fg, bg=label_bg, 
                font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_usuario = tk.Entry(self.root, bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_usuario.pack(pady=5)
        
        tk.Label(self.root, text="🔑 Contraseña:", fg=label_fg, bg=label_bg, 
                font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_contraseña = tk.Entry(self.root, show="*", bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_contraseña.pack(pady=5)
        
        # Botones
        tk.Button(self.root, text="🚀 Ingresar", command=self.verificar_login, 
                 bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
        tk.Button(self.root, text="✨ Registrarse", command=self.registrar_nuevo_usuario, 
                 bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
        tk.Button(self.root, text="😎 Face ID", command=iniciar_face_recognition, 
                 bg="#27AE60", fg="white", font=button_font).pack(pady=5)
        tk.Button(self.root, text="❌ Salir", bg="#E74C3C", fg="white", 
                 font=button_font, command=self.root.quit).pack(pady=5)
    
    def verificar_login(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        if self.gestor.validar_usuario(usuario, contraseña):
            messagebox.showinfo("🎉 Éxito", "¡Login exitoso! 🥳")
        else:
            messagebox.showerror("⚠️ Error", "Usuario o contraseña incorrectos 😕")
    
    def registrar_nuevo_usuario(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        if not usuario or not contraseña:
            messagebox.showwarning("🤔 Advertencia", "Debe ingresar usuario y contraseña")
            return
        
        if self.gestor.registrar_usuario(usuario, contraseña):
            messagebox.showinfo("🎊 Registro", "¡Usuario registrado con éxito! 🎈")
        else:
            messagebox.showerror("😣 Error", "El usuario ya existe")


if __name__ == "__main__":
    root = tk.Tk()
    # Usar la versión mejorada
    app = LoginAppMejorado(root)
    root.resizable(False, False)
=======
        # Llamamos a la función main_gui del módulo face_gui
        face_gui.main_gui()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.resizable(False, False) 
>>>>>>> origin/main
    root.mainloop()