import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0

    def agregar_punto(self):
        self.puntos += 1

class Temporizador:
    def __init__(self, etiqueta, ventana):
        self.etiqueta = etiqueta
        self.ventana = ventana
        self.segundos = 10
        self.actualizando = True

    def iniciar(self):
        self.actualizando = True
        self.actualizar()

    def detener(self):
        self.actualizando = False

    def actualizar(self):
        if self.actualizando:
            self.etiqueta.config(text=f"Tiempo: {self.segundos} s")
            self.segundos -= 1
            self.ventana.after(1000, self.actualizar)

class VentanaJuego:
    def __init__(self, ventana_anterior):
        self.ventana_anterior = ventana_anterior
        self.ventana = tk.Toplevel()
        self.ventana.title("Juego de Memoria")
        self.ventana.geometry("1000x820")
        self.ventana.configure(bg="#f3f3f3")

        self.filas = 6
        self.columnas = 6
        self.boton_size = 90

        self.jugadores = [Jugador("Jugador 1"), Jugador("Jugador 2")]
        self.turno_actual = 0

        self.matrices_jugadores = [[], []]
        self.imagenes_jugadores = [[], []]

        self.celdas_reveladas = []
        self.total_parejas = (self.filas * self.columnas) // 2
        self.parejas_encontradas = 0

        self.crear_interfaz()
        imagenes_por_jugador = self.cargar_imagenes()

        for jugador_idx in range(2):
            self.imagenes_jugadores[jugador_idx] = self.asignar_imagenes(imagenes_por_jugador[jugador_idx])
            self.matrices_jugadores[jugador_idx] = self.crear_matriz(jugador_idx)

        self.temporizador.iniciar()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cargar_imagenes(self):
        ruta_img = "IMG"
        nombres_png = [nombre for nombre in os.listdir(ruta_img) if nombre.endswith(".png")]
        nombres_png = nombres_png[:self.total_parejas * 2]
        random.shuffle(nombres_png)

        imagenes_jugadores = []
        for i in range(2):
            imagenes_temp = []
            nombres_jugador = nombres_png[i*18:(i+1)*18]
            for nombre in nombres_jugador:
                ruta = os.path.join(ruta_img, nombre)
                imagen = Image.open(ruta).resize((self.boton_size, self.boton_size))
                imagen_tk = ImageTk.PhotoImage(imagen)
                imagenes_temp.append(imagen_tk)
                imagenes_temp.append(imagen_tk)
            random.shuffle(imagenes_temp)
            imagenes_jugadores.append(imagenes_temp)
        return imagenes_jugadores

    def asignar_imagenes(self, imagenes):
        matriz = []
        idx = 0
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(imagenes[idx])
                idx += 1
            matriz.append(fila)
        return matriz

    def crear_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana, bg="#f3f3f3")
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame_principal, height=50, bg="#858386")
        self.frame_info.pack(side="top", fill="x")

        self.etiqueta_info = tk.Label(self.frame_info, text="", bg="#858386", fg="white", font=("Arial", 14))
        self.etiqueta_info.pack(pady=10, side="left", padx=20)

        self.etiqueta_tiempo = tk.Label(self.frame_info, text="Tiempo: 0 s", bg="#858386", fg="white", font=("Arial", 14))
        self.etiqueta_tiempo.pack(side="right", padx=10)

        self.temporizador = Temporizador(self.etiqueta_tiempo, self.ventana)

        self.frames_matrices = []
        frame_matrices_container = tk.Frame(self.frame_principal, bg="#696969")
        frame_matrices_container.pack(expand=True, pady=(10, 20))

        for i in range(2):
            frame = tk.Frame(frame_matrices_container, bg="#696969")
            frame.grid(row=0, column=i, padx=20)
            self.frames_matrices.append(frame)

        self.actualizar_info_turno()

    def crear_matriz(self, jugador_idx):
        botones = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                frame_celda = tk.Frame(self.frames_matrices[jugador_idx], width=self.boton_size, height=self.boton_size, bg="#f3f3f3")
                frame_celda.grid(row=i, column=j, padx=6, pady=6)
                frame_celda.propagate(False)

                boton = tk.Button(frame_celda,
                                bg="#ffffff",
                                relief="flat",
                                bd=0,
                                highlightthickness=0,
                                activebackground="#e6e6e6",
                                command=lambda f=i, c=j, jidx=jugador_idx: self.revelar_imagen(f, c, jidx))
                boton.pack(fill="both", expand=True)
                fila.append(boton)
            botones.append(fila)
        return botones

    def revelar_imagen(self, fila, col, jugador_idx):
        if jugador_idx != self.turno_actual or len(self.celdas_reveladas) >= 2:
            return

        boton = self.matrices_jugadores[jugador_idx][fila][col]
        if boton["state"] == "disabled" or (fila, col) in self.celdas_reveladas:
            return

        imagen = self.imagenes_jugadores[jugador_idx][fila][col]
        boton.config(image=imagen)
        self.celdas_reveladas.append((fila, col))

        if len(self.celdas_reveladas) == 2:
            self.ventana.after(800, lambda: self.verificar_coincidencia(jugador_idx))

    def verificar_coincidencia(self, jugador_idx):
        (f1, c1), (f2, c2) = self.celdas_reveladas
        img1 = self.imagenes_jugadores[jugador_idx][f1][c1]
        img2 = self.imagenes_jugadores[jugador_idx][f2][c2]

        if img1 == img2:
            self.matrices_jugadores[jugador_idx][f1][c1].config(state="disabled")
            self.matrices_jugadores[jugador_idx][f2][c2].config(state="disabled")
            self.jugadores[jugador_idx].agregar_punto()
            self.parejas_encontradas += 1
        else:
            self.matrices_jugadores[jugador_idx][f1][c1].config(image='')
            self.matrices_jugadores[jugador_idx][f2][c2].config(image='')
            self.turno_actual = 1 - self.turno_actual

        self.celdas_reveladas.clear()
        self.actualizar_info_turno()

        if self.parejas_encontradas == self.total_parejas * 2:
            self.temporizador.detener()
            ganador = max(self.jugadores, key=lambda j: j.puntos)
            empates = [j for j in self.jugadores if j.puntos == ganador.puntos]
            if len(empates) > 1:
                mensaje = "\u00a1Empate!"
            else:
                mensaje = f"\u00a1{ganador.nombre} ha ganado con {ganador.puntos} puntos!"
            messagebox.showinfo("Fin del juego", mensaje)

    def actualizar_info_turno(self):
        j1, j2 = self.jugadores
        texto = f"{j1.nombre}: {j1.puntos} pts   |   {j2.nombre}: {j2.puntos} pts   |   Turno: {self.jugadores[self.turno_actual].nombre}"
        self.etiqueta_info.config(text=texto)

        for idx, frame in enumerate(self.frames_matrices):
            if idx == self.turno_actual:
                frame.config(bg="#696969")
            else:
                frame.config(bg="#999999")  # desactiva visualmente el tablero del otro jugador

    def cerrar_ventana(self):
        self.ventana.destroy()
        self.ventana_anterior.deiconify()
