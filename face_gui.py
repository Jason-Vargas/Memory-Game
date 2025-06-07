import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
import threading
import time

# --- Tu clase FaceRecognitionSystem ---

class FaceRecognitionSystem:
    def __init__(self, users_dir="users_lbph"):
        self.users_dir = users_dir
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)

    # ... (tu código de registro y carga de rostros igual)

    def login_with_face(self, timeout=15):
        known_encodings, known_names = self.load_known_faces()
        if not known_encodings:
            messagebox.showerror("Error", "No hay rostros registrados.")
            return None

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return None

        start_time = time.time()
        recognized_user = None

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], (100, 100)).flatten()
                    name, confidence = self._recognize_face(face, known_encodings, known_names)

                    if name:
                        label = f"Reconocido: {name}"
                        color = (0, 255, 0)
                        recognized_user = name
                    else:
                        label = "Desconocido"
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    if recognized_user:
                        # Espera 1 segundo para mostrar el rectángulo verde
                        cv2.imshow("Login con rostro", frame)
                        cv2.waitKey(1000)
                        cap.release()
                        cv2.destroyAllWindows()
                        return recognized_user  # Retorna el nombre reconocido

                cv2.imshow("Login con rostro", frame)

                if time.time() - start_time > timeout:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

        return None

    # ... resto de métodos (register_face, load_known_faces, etc.)

# --- Tu GUI principal ---

class FaceRecognitionGUI:
    def __init__(self):
        self.face_system = FaceRecognitionSystem()
        self.root = tk.Tk()
        self.root.title("Sistema de Reconocimiento Facial (LBPH)")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.ventana_principal = None  # Guardaremos la ventana principal aquí

        self.setup_gui()

    def setup_gui(self):
        title_label = tk.Label(
            self.root,
            text="Reconocimiento Facial (OpenCV + LBPH)",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=15)

        btn_register = tk.Button(
            self.root,
            text="Registrar nuevo rostro",
            command=self.register_face_gui,
            width=30, height=2,
            bg="#4CAF50", fg="white",
            font=("Arial", 10)
        )
        btn_register.pack(pady=10)

        btn_login = tk.Button(
            self.root,
            text="Iniciar sesión con rostro",
            command=self.login_with_face_threaded,
            width=30, height=2,
            bg="#2196F3", fg="white",
            font=("Arial", 10)
        )
        btn_login.pack(pady=10)

        btn_users = tk.Button(
            self.root,
            text="Ver usuarios registrados",
            command=self.show_registered_users,
            width=30, height=2,
            bg="#FF9800", fg="white",
            font=("Arial", 10)
        )
        btn_users.pack(pady=10)

        btn_exit = tk.Button(
            self.root,
            text="Salir",
            command=self.root.destroy,
            width=30, height=2,
            bg="#f44336", fg="white",
            font=("Arial", 10)
        )
        btn_exit.pack(pady=10)

    def register_face_gui(self):
        self.face_system.register_face()

    def show_registered_users(self):
        users = self.face_system.get_registered_users()
        if users:
            user_list = "\n".join([f"• {user}" for user in users])
            messagebox.showinfo("Usuarios Registrados", f"Usuarios en el sistema:\n\n{user_list}")
        else:
            messagebox.showinfo("Usuarios Registrados", "No hay usuarios registrados en el sistema.")

    def on_login_success(self, username):
        messagebox.showinfo("Login exitoso", f"Bienvenido, {username}!")
        # Importar aquí para evitar ciclos
        from ventana import VentanaPrincipal
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.ejecutar()

    def login_with_face_threaded(self):
        def login_thread():
            username = self.face_system.login_with_face()
            if username:
                # Ejecutar en hilo principal de Tkinter para evitar errores con la GUI
                self.root.after(0, self.on_login_success, username)
            else:
                self.root.after(0, lambda: messagebox.showinfo("Login fallido", "No se reconoció ningún rostro o se canceló el login."))

        threading.Thread(target=login_thread, daemon=True).start()

    def run(self):
        self.root.mainloop()


def main():
    app = FaceRecognitionGUI()
    app.run()

if __name__ == "__main__":
    main()
