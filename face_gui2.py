import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
import threading
import time


class FaceRecognitionSystem:
    def __init__(self, users_dir="users_lbph"):
        """
        Inicializa el sistema de reconocimiento facial.
        
        Args:
            users_dir (str): Directorio donde se almacenan los datos de usuarios
        """
        self.users_dir = users_dir
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self._ensure_users_directory()
    
    def _ensure_users_directory(self):
        """Crea el directorio de usuarios si no existe."""
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)
    
    def register_face(self, name=None):
        """
        Registra un nuevo rostro en el sistema.
        
        Args:
            name (str, optional): Nombre del usuario. Si no se proporciona, se solicita via GUI.
        
        Returns:
            bool: True si el registro fue exitoso, False en caso contrario.
        """
        if name is None:
            name = simpledialog.askstring("Registro", "Ingresa tu nombre de usuario:")
        
        if not name:
            messagebox.showerror("Error", "Nombre inválido.")
            return False

        name = name.strip().lower()
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return False

        count = 0
        faces_data = []
        
        messagebox.showinfo("Instrucción", "Mira a la cámara. Se capturarán 10 imágenes automáticamente.")

        try:
            while count < 10:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "No se pudo leer de la cámara.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face, (100, 100))
                    faces_data.append(face_resized)
                    count += 1

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Captura {count}/10", (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                cv2.imshow("Registrando rostro", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

        if faces_data:
            mean_face = np.mean(faces_data, axis=0)
            filepath = os.path.join(self.users_dir, f"{name}.npy")
            np.save(filepath, mean_face)
            messagebox.showinfo("Éxito", f"Rostro guardado correctamente como '{filepath}'")
            return True
        else:
            messagebox.showwarning("Sin capturas", "No se capturó ningún rostro.")
            return False
    
    def load_known_faces(self):
        """
        Carga todos los rostros conocidos desde el directorio de usuarios.
        
        Returns:
            tuple: (encodings, names) - Listas de encodings y nombres correspondientes
        """
        encodings = []
        names = []

        for file in os.listdir(self.users_dir):
            if file.endswith(".npy"):
                path = os.path.join(self.users_dir, file)
                try:
                    encoding = np.load(path).flatten()
                    encodings.append(encoding)
                    names.append(os.path.splitext(file)[0])
                except Exception as e:
                    print(f"Error cargando {file}: {e}")

        return encodings, names
    
    def _recognize_face(self, face_encoding, known_encodings, known_names, threshold=2000):
        """
        Reconoce un rostro comparándolo con los rostros conocidos.
        
        Args:
            face_encoding: Encoding del rostro a reconocer
            known_encodings: Lista de encodings conocidos
            known_names: Lista de nombres correspondientes a los encodings
            threshold: Umbral de distancia para considerar una coincidencia
        
        Returns:
            tuple: (nombre_reconocido, confianza) o (None, None) si no se reconoce
        """
        if not known_encodings:
            return None, None
        
        distances = [np.linalg.norm(face_encoding - known_enc) for known_enc in known_encodings]
        min_distance = min(distances)
        best_match_index = np.argmin(distances)
        
        if min_distance < threshold:
            return known_names[best_match_index], min_distance
        else:
            return None, min_distance
    
    def login_with_face(self, timeout=15):
        """
        Intenta hacer login usando reconocimiento facial.
        
        Args:
            timeout (int): Tiempo límite en segundos para el reconocimiento
        
        Returns:
            str or None: Nombre del usuario reconocido o None si falla
        """
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
                        cv2.imshow("Login con rostro", frame)
                        cv2.waitKey(1000)
                        messagebox.showinfo("Login exitoso", f"Bienvenido, {name}!")
                        return recognized_user

                cv2.imshow("Login con rostro", frame)

                if time.time() - start_time > timeout:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

        messagebox.showinfo("Login fallido", "No se reconoció ningún rostro o se canceló el login.")
        return None
    
    def login_with_face_threaded(self):
        """Ejecuta el login con rostro en un hilo separado para no bloquear la GUI."""
        def login_thread():
            try:
                self.login_with_face()
            except Exception as e:
                messagebox.showerror("Error inesperado", str(e))
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def get_registered_users(self):
        """
        Obtiene la lista de usuarios registrados.
        
        Returns:
            list: Lista de nombres de usuarios registrados
        """
        users = []
        for file in os.listdir(self.users_dir):
            if file.endswith(".npy"):
                users.append(os.path.splitext(file)[0])
        return users
    
    def delete_user(self, username):
        """
        Elimina un usuario del sistema.
        
        Args:
            username (str): Nombre del usuario a eliminar
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        filepath = os.path.join(self.users_dir, f"{username.lower()}.npy")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                print(f"Error eliminando usuario {username}: {e}")
                return False
        return False


class FaceRecognitionGUI:
    def __init__(self):
        """Inicializa la interfaz gráfica del sistema de reconocimiento facial."""
        self.face_system = FaceRecognitionSystem()
        self.root = tk.Tk()
        self.setup_gui()
    
    def setup_gui(self):
        """Configura la interfaz gráfica."""
        self.root.title("Sistema de Reconocimiento Facial (LBPH)")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Título
        title_label = tk.Label(
            self.root, 
            text="Reconocimiento Facial (OpenCV + LBPH)", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=15)
        
        # Botones principales
        btn_register = tk.Button(
            self.root, 
            text="Registrar nuevo rostro", 
            command=self.register_face_gui,
            width=30, 
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10)
        )
        btn_register.pack(pady=10)
        
        btn_login = tk.Button(
            self.root, 
            text="Iniciar sesión con rostro", 
            command=self.login_with_face_gui,
            width=30, 
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        )
        btn_login.pack(pady=10)
        
        btn_users = tk.Button(
            self.root, 
            text="Ver usuarios registrados", 
            command=self.show_registered_users,
            width=30, 
            height=2,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10)
        )
        btn_users.pack(pady=10)
        
        btn_exit = tk.Button(
            self.root, 
            text="Salir", 
            command=self.root.destroy,
            width=30, 
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 10)
        )
        btn_exit.pack(pady=10)
    
    def register_face_gui(self):
        """Maneja el registro de rostro desde la GUI."""
        self.face_system.register_face()
    
    def login_with_face_gui(self):
        """Maneja el login con rostro desde la GUI."""
        self.face_system.login_with_face_threaded()
    
    def show_registered_users(self):
        """Muestra la lista de usuarios registrados."""
        users = self.face_system.get_registered_users()
        if users:
            user_list = "\n".join([f"• {user}" for user in users])
            messagebox.showinfo("Usuarios Registrados", f"Usuarios en el sistema:\n\n{user_list}")
        else:
            messagebox.showinfo("Usuarios Registrados", "No hay usuarios registrados en el sistema.")
    
    def run(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()


def main():
    """Función principal para ejecutar la aplicación."""
    app = FaceRecognitionGUI()
    app.run()


if __name__ == "__main__":
    main()