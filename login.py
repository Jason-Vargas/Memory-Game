import tkinter as tk
from tkinter import messagebox
from logica import GestorUsuarios  # Lógica de usuarios
from ventana import VentanaPrincipal  # Ventana principal a mostrar tras login
import face_gui2  # Módulo para reconocimiento facial
from APIBCCR import *

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 ¡Bienvenido! 🎉")
        self.root.geometry("350x400")
        self.root.configure(bg="#3BDBFF")
        
        self.gestor = GestorUsuarios()
        
        label_fg = "#4A148C"
        label_bg = "#3BC1FF"
        entry_bg = "#FFF"
        button_bg = "#6200EA"
        button_fg = "white"
        button_font = ("Comic Sans MS", 12, "bold")
        
        tk.Label(self.root, text="👤 Usuario:", fg=label_fg, bg=label_bg, font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_usuario = tk.Entry(self.root, bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_usuario.pack(pady=5)
        
        tk.Label(self.root, text="🔑 Contraseña:", fg=label_fg, bg=label_bg, font=("Comic Sans MS", 12, "bold")).pack(pady=5)
        self.entrada_contraseña = tk.Entry(self.root, show="*", bg=entry_bg, font=("Comic Sans MS", 12))
        self.entrada_contraseña.pack(pady=5)
        
        tk.Button(self.root, text="🚀 Ingresar", command=self.verificar_login, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
        tk.Button(self.root, text="✨ Registrarse", command=self.registrar_nuevo_usuario, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
        tk.Button(self.root, text="😎 Face ID", command=self.iniciar_sesion_face_id, bg="#27AE60", fg="white", font=button_font).pack(pady=5)
        tk.Button(self.root, text="❌ Salir", bg="#E74C3C", fg="white", font=button_font, command=self.root.quit).pack(pady=5)

    def verificar_login(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()
        
        if self.gestor.validar_usuario(usuario, contraseña):
            messagebox.showinfo("🎉 Éxito", "¡Login exitoso! 🥳")
            self.root.destroy()
            ventana = VentanaPrincipal()
            ventana.ejecutar()
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
        """Inicia el reconocimiento facial y abre ventana principal si es exitoso."""
        try:
            # Supongamos que face_gui2.main_gui() retorna True si fue exitoso
            resultado = False
            
            if hasattr(face_gui2, 'main_gui'):
                resultado = face_gui2.main_gui()
            elif hasattr(face_gui2, 'main'):
                resultado = face_gui2.main()
            else:
                messagebox.showerror("Error", "No se encontró función para Face ID")
                return
            
            if resultado:
                messagebox.showinfo("🎉 Éxito", "¡Login con Face ID exitoso! 🥳")
                self.root.destroy()
                ventana = VentanaPrincipal()
                ventana.ejecutar()
            else:
                messagebox.showerror("⚠️ Error", "Reconocimiento facial fallido 😕")
        except Exception as e:
            messagebox.showerror("Error Face ID", f"Error al iniciar Face ID: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.resizable(False, False)
    root.mainloop()
