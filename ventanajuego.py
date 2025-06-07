import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import os

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0

    def agregar_punto(self):
        self.puntos += 1

class Bot(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)

    def seleccionar_cartas(self, matriz_botones, imagenes, filas, columnas):
        disponibles = []
        for i in range(filas):
            for j in range(columnas):
                boton = matriz_botones[i][j]
                if boton["state"] != "disabled" and boton.cget("image") == "":
                    disponibles.append((i, j))
        if len(disponibles) < 2:
            return []
        return random.sample(disponibles, 2)

class Temporizador:
    def __init__(self, barra_progreso, ventana, callback_tiempo_agotado):
        self.barra = barra_progreso
        self.ventana = ventana
        self.segundos_totales = 10
        self.segundos_restantes = self.segundos_totales
        self.actualizando = False
        self.callback_tiempo_agotado = callback_tiempo_agotado
        self._job = None  # Para guardar el after y poder cancelarlo

    def iniciar(self):
        self.detener()  # Por si ya estaba corriendo
        self.segundos_restantes = self.segundos_totales
        self.barra['maximum'] = self.segundos_totales
        self.barra['value'] = self.segundos_totales
        self.actualizando = True
        self._programar_actualizacion()

    def detener(self):
        self.actualizando = False
        if self._job is not None:
            self.ventana.after_cancel(self._job)
            self._job = None

    def reiniciar(self):
        self.iniciar()

    def _programar_actualizacion(self):
        if not self.actualizando:
            return
        if self.segundos_restantes <= 0:
            self.actualizando = False
            self.callback_tiempo_agotado()
            return
        self.barra['value'] = self.segundos_restantes
        self.segundos_restantes -= 1
        self._job = self.ventana.after(1000, self._programar_actualizacion)


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

        self.jugadores = [Jugador("Jugador 1"), Bot("Jugador 2 (Bot)")]
        self.turno_actual = 0

        self.matrices_jugadores = [[], []]
        self.imagenes_jugadores = []

        self.celdas_reveladas = []
        self.total_parejas = (self.filas * self.columnas) // 2
        self.parejas_encontradas = 0

        self.crear_interfaz()
        imagenes = self.cargar_imagenes()

        for _ in range(2):
            imgs = imagenes[:]
            random.shuffle(imgs)
            self.imagenes_jugadores.append(self.asignar_imagenes(imgs))

        for jugador_idx in range(2):
            self.matrices_jugadores[jugador_idx] = self.crear_matriz(jugador_idx)

        self.mostrar_tablero(self.turno_actual)

        self.temporizador = Temporizador(self.barra_tiempo, self.ventana, self.tiempo_agotado)
        self.temporizador.iniciar()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        if isinstance(self.jugadores[self.turno_actual], Bot):
            self.ventana.after(1000, self.turno_bot)

    def cargar_imagenes(self):
        ruta_img = "IMG"
        nombres_png = [nombre for nombre in os.listdir(ruta_img) if nombre.endswith(".png")]
        nombres_png = nombres_png[:self.total_parejas]
        imagenes_temp = []
        for nombre in nombres_png:
            ruta = os.path.join(ruta_img, nombre)
            imagen = Image.open(ruta).resize((self.boton_size, self.boton_size))
            imagen_tk = ImageTk.PhotoImage(imagen)
            imagenes_temp.append(imagen_tk)
            imagenes_temp.append(imagen_tk)
        random.shuffle(imagenes_temp)
        return imagenes_temp

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

        self.barra_tiempo = ttk.Progressbar(self.frame_info, orient="horizontal", length=200, mode="determinate")
        self.barra_tiempo.pack(side="right", padx=20, pady=10)

        self.frames_matrices = []
        frame_matrices_container = tk.Frame(self.frame_principal, bg="#696969")
        frame_matrices_container.pack(expand=True, pady=(10, 20))

        colores_fondo = ["#007FFF", "#FF4040"]

        for i in range(2):
            frame = tk.Frame(frame_matrices_container, bg=colores_fondo[i])
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
        if jugador_idx != self.turno_actual or isinstance(self.jugadores[jugador_idx], Bot) or len(self.celdas_reveladas) >= 2:
            return

        boton = self.matrices_jugadores[jugador_idx][fila][col]
        if boton["state"] == "disabled" or (fila, col) in self.celdas_reveladas:
            return

        imagen = self.imagenes_jugadores[jugador_idx][fila][col]
        boton.config(image=imagen)
        boton.image = imagen
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
            for (f, c) in [(f1, c1), (f2, c2)]:
                boton = self.matrices_jugadores[jugador_idx][f][c]
                boton.config(image='')
                boton.image = None

            self.turno_actual = 1 - self.turno_actual
            self.mostrar_tablero(self.turno_actual)
            self.temporizador.reiniciar()
            self.temporizador.iniciar()

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
        else:
            if isinstance(self.jugadores[self.turno_actual], Bot):
                self.ventana.after(1000, self.turno_bot)

    def mostrar_tablero(self, jugador_idx):
        for i, frame in enumerate(self.frames_matrices):
            if i == jugador_idx:
                frame.tkraise()
                frame.lift()
                frame.grid()
            else:
                frame.grid_remove()

    def actualizar_info_turno(self):
        j1, j2 = self.jugadores
        texto = f"{j1.nombre}: {j1.puntos} pts   |   {j2.nombre}: {j2.puntos} pts   |   Turno: {self.jugadores[self.turno_actual].nombre}"
        self.etiqueta_info.config(text=texto)

    def turno_bot(self):
        jugador_idx = self.turno_actual
        bot = self.jugadores[jugador_idx]
        botones = self.matrices_jugadores[jugador_idx]

        pares = bot.seleccionar_cartas(botones, self.imagenes_jugadores[jugador_idx], self.filas, self.columnas)
        if len(pares) < 2:
            return

        f1, c1 = pares[0]
        boton1 = botones[f1][c1]
        boton1.config(image=self.imagenes_jugadores[jugador_idx][f1][c1])
        boton1.image = self.imagenes_jugadores[jugador_idx][f1][c1]
        self.celdas_reveladas.append((f1, c1))

        def revelar_segunda():
            f2, c2 = pares[1]
            boton2 = botones[f2][c2]
            boton2.config(image=self.imagenes_jugadores[jugador_idx][f2][c2])
            boton2.image = self.imagenes_jugadores[jugador_idx][f2][c2]
            self.celdas_reveladas.append((f2, c2))
            self.ventana.after(1000, lambda: self.verificar_coincidencia(jugador_idx))

        self.ventana.after(1000, revelar_segunda)

    def tiempo_agotado(self):
        messagebox.showinfo("Tiempo agotado", f"Tiempo terminado. Cambia turno.")
        self.turno_actual = 1 - self.turno_actual
        self.mostrar_tablero(self.turno_actual)
        self.temporizador.reiniciar()
        self.temporizador.iniciar()
        self.actualizar_info_turno()

        if isinstance(self.jugadores[self.turno_actual], Bot):
            self.ventana.after(1000, self.turno_bot)

    def cerrar_ventana(self):
        self.temporizador.detener()
        self.ventana.destroy()
        self.ventana_anterior.deiconify()

