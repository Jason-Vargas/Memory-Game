import tkinter as tk
from tkinter import messagebox
import threading
import time
from game_logic import PatternGame
from APIBCCR import TipoCambioBCCR

def mostrar_tipo_cambio_hoy(correo_api, token_api):
    """
    Función que solo imprime el tipo de cambio del dólar del día de hoy en la terminal.
    
    Args:
        correo_api (str): Correo electrónico registrado en el BCCR
        token_api (str): Token de API del BCCR
    """
    try:
        # Verificar credenciales primero
        if not correo_api or correo_api == "tu_correo@ejemplo.com":
            print("❌ Error: Debes configurar tu correo real del BCCR")
            print("   Cambia 'tu_correo@ejemplo.com' por tu correo registrado")
            return
            
        if not token_api or token_api == "tu_token_aqui":
            print("❌ Error: Debes configurar tu token real del BCCR")
            print("   Cambia 'tu_token_aqui' por tu token de la API")
            return
        
        print(f"🔑 Usando correo: {correo_api}")
        print("🔑 Token configurado ✓")
        
        # Crear instancia del cliente BCCR
        bccr = TipoCambioBCCR(correo_api, token_api)
        print("📡 Conectando con BCCR...")
        
        # Obtener tipo de cambio de venta del día
        tipo_cambio = bccr.obtener_venta()
        
        print(f"📊 Respuesta de la API: {tipo_cambio}")
        
        if not tipo_cambio or tipo_cambio <= 0:
            print("❌ No se pudo obtener el tipo de cambio")
            print("   Posibles causas:")
            print("   • Credenciales incorrectas")
            print("   • Token expirado")
            print("   • Problema de conexión")
            print("   • API del BCCR temporalmente no disponible")
            return
            
        print(f"💱 Tipo de cambio del dólar hoy: ₡{tipo_cambio:.2f}")
        
    except ImportError:
        print("❌ Error: No se pudo importar el módulo APIBCCR")
        print("   Asegúrate de que el archivo APIBCCR.py esté en la misma carpeta")
    except Exception as e:
        print(f"❌ Error detallado: {type(e).__name__}: {e}")
        print("   Revisa tus credenciales y conexión a internet")


def guardar_mejores_resultados(score, valor_usd, archivo="mejores_resultados.txt"):
    nuevo_resultado = (score, valor_usd)

    # Leer resultados anteriores
    resultados = []
    try:
        with open(archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split(" - Valor: $")
                if len(partes) == 2:
                    puntaje = int(partes[0].replace("Puntaje: ", ""))
                    valor = float(partes[1].replace(" USD", ""))
                    resultados.append((puntaje, valor))
    except FileNotFoundError:
        pass  # Si no existe, se crea después

    # Agregar nuevo resultado y ordenar por valor_usd descendente
    resultados.append(nuevo_resultado)
    resultados.sort(key=lambda x: x[1], reverse=True)

    # Mantener solo los 5 mejores
    mejores = resultados[:5]

    # Guardar en el archivo
    with open(archivo, "w") as f:
        for puntaje, valor in mejores:
            f.write(f"Puntaje: {puntaje} - Valor: ${valor:.2f} USD\n")


class PatternGameGUI:
    def __init__(self, correo_api=None, token_api=None):
        self.root = tk.Tk()
        self.root.title("Juego de Patrones - Con Timer")
        self.root.geometry("800x750")
        self.root.configure(bg='#2c3e50')
        
        # Configuración API para BCCR
        self.correo_api = correo_api
        self.token_api = token_api
        
        # Variables de interfaz
        self.buttons = {}
        
        # Instancia del juego con callback
        self.game = PatternGame(ui_callback=self.handle_game_event)
        
        self.setup_ui()
        
    def handle_game_event(self, event_type, data=None):
        """Maneja todos los eventos que vienen de la lógica del juego"""
        if event_type == 'game_started':
            self.on_game_started(data)
        elif event_type == 'update_display':
            self.update_display(data)
        elif event_type == 'start_pattern_display':
            self.start_pattern_animation(data)
        elif event_type == 'enable_player_input':
            self.enable_player_input(data)
        elif event_type == 'game_over':
            self.show_game_over(data)
        elif event_type == 'victory':
            self.show_victory(data)
        elif event_type == 'level_completed':
            self.on_level_completed()
        elif event_type == 'schedule_next_pattern':
            self.schedule_next_pattern(data['delay'])
        elif event_type == 'time_update':
            self.update_timer_display(data['remaining_time'])
        elif event_type == 'timeout_game_over':
            self.show_timeout_game_over(data)
            
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Título
        title_label = tk.Label(
            self.root, 
            text="🎮 JUEGO DE PATRONES - CON TIMER 🎮", 
            font=('Arial', 18, 'bold'),
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Frame de información
        self.info_frame = tk.Frame(self.root, bg='#2c3e50')
        self.info_frame.pack(pady=10)
        
        self.level_label = tk.Label(
            self.info_frame, 
            text="Nivel: 1", 
            font=('Arial', 14),
            bg='#2c3e50', 
            fg='white'
        )
        self.level_label.pack(side=tk.LEFT, padx=15)
        
        self.score_label = tk.Label(
            self.info_frame, 
            text="Puntuación: 0", 
            font=('Arial', 14),
            bg='#2c3e50', 
            fg='white'
        )
        self.score_label.pack(side=tk.LEFT, padx=15)
        
        # Timer display
        self.timer_label = tk.Label(
            self.info_frame,
            text="Tiempo: --",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='#f39c12'
        )
        self.timer_label.pack(side=tk.LEFT, padx=15)
        
        # Frame de instrucciones
        self.instruction_label = tk.Label(
            self.root, 
            text="¡Presiona 'NUEVO JUEGO' para comenzar!", 
            font=('Arial', 13, 'bold'),
            bg='#2c3e50', 
            fg='#f39c12'
        )
        self.instruction_label.pack(pady=10)
        
        # Frame de reglas
        rules_frame = tk.Frame(self.root, bg='#2c3e50')
        rules_frame.pack(pady=5)
        
        rules_text = "📋 REGLAS: Empieza con 3 casillas • Máximo 12 segundos total • Máximo 2 segundos entre casillas"
        self.rules_label = tk.Label(
            rules_frame,
            text=rules_text,
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#bdc3c7',
            wraplength=700
        )
        self.rules_label.pack()
        
        # Frame de botones de colores
        self.game_frame = tk.Frame(self.root, bg='#2c3e50')
        self.game_frame.pack(pady=20)
        
        # Configuración de colores y posiciones para 4x4
        color_config = {
            'red': {'row': 0, 'col': 0, 'bg': '#e74c3c', 'active_bg': '#ff6b6b'},
            'blue': {'row': 0, 'col': 1, 'bg': '#3498db', 'active_bg': '#5dade2'},
            'green': {'row': 0, 'col': 2, 'bg': '#2ecc71', 'active_bg': '#58d68d'},
            'yellow': {'row': 0, 'col': 3, 'bg': '#f1c40f', 'active_bg': '#f7dc6f'},
            'orange': {'row': 1, 'col': 0, 'bg': '#e67e22', 'active_bg': '#f39c12'},
            'purple': {'row': 1, 'col': 1, 'bg': '#9b59b6', 'active_bg': '#bb77d9'},
            'pink': {'row': 1, 'col': 2, 'bg': '#e91e63', 'active_bg': '#f06292'},
            'cyan': {'row': 1, 'col': 3, 'bg': '#1abc9c', 'active_bg': '#48c9b0'},
            'lime': {'row': 2, 'col': 0, 'bg': '#8bc34a', 'active_bg': '#aed581'},
            'magenta': {'row': 2, 'col': 1, 'bg': '#d81b60', 'active_bg': '#f06292'},
            'brown': {'row': 2, 'col': 2, 'bg': '#795548', 'active_bg': '#a1887f'},
            'navy': {'row': 2, 'col': 3, 'bg': '#2c3e50', 'active_bg': '#34495e'},
            'olive': {'row': 3, 'col': 0, 'bg': '#827717', 'active_bg': '#9e9d24'},
            'maroon': {'row': 3, 'col': 1, 'bg': '#880e4f', 'active_bg': '#ad1457'},
            'teal': {'row': 3, 'col': 2, 'bg': '#00695c', 'active_bg': '#00897b'},
            'silver': {'row': 3, 'col': 3, 'bg': '#9e9e9e', 'active_bg': '#bdbdbd'}
        }
        
        # Crear botones de colores 4x4
        for color, config in color_config.items():
            btn = tk.Button(
                self.game_frame,
                width=10,
                height=5,
                bg=config['bg'],
                activebackground=config['active_bg'],
                relief='raised',
                bd=3,
                command=lambda c=color: self.on_color_button_clicked(c),
                state='disabled'
            )
            btn.grid(row=config['row'], column=config['col'], padx=5, pady=5)
            self.buttons[color] = btn
            
        # Frame de controles
        self.control_frame = tk.Frame(self.root, bg='#2c3e50')
        self.control_frame.pack(pady=15)
        
        self.new_game_btn = tk.Button(
            self.control_frame,
            text="🎲 NUEVO JUEGO",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=25,
            pady=12,
            command=self.on_new_game_clicked
        )
        self.new_game_btn.pack()
        
    # === MANEJADORES DE EVENTOS DE UI ===
    def on_new_game_clicked(self):
        """Se ejecuta cuando se presiona el botón de nuevo juego"""
        self.game.start_new_game()
            
    def on_color_button_clicked(self, color):
        """Se ejecuta cuando se presiona un botón de color"""
        # Efecto visual inmediato
        self.flash_button(color)
        # Enviar entrada al juego
        self.game.add_player_input(color)
        
    # === MANEJADORES DE EVENTOS DEL JUEGO ===
    def on_game_started(self, game_state):
        """Se ejecuta cuando el juego inicia"""
        self.instruction_label.config(text="¡Preparando patrón inicial de 3 casillas!")
        self.timer_label.config(text="Tiempo: --", fg='#f39c12')
        
    def start_pattern_animation(self, data):
        """Inicia la animación del patrón"""
        self.disable_all_inputs()
        self.instruction_label.config(text=f"¡Observa atentamente el patrón de {len(data['sequence'])} casillas!")
        self.timer_label.config(text="Tiempo: --", fg='#f39c12')
        
        # Ejecutar animación en hilo separado
        threading.Thread(
            target=self._animate_pattern, 
            args=(data['sequence'], data['speed']), 
            daemon=True
        ).start()
        
    def enable_player_input(self, game_state):
        """Habilita la entrada del jugador"""
        self.enable_color_buttons()
        self.instruction_label.config(text=f"¡Repite el patrón de {game_state['sequence_length']} casillas! (12 seg total, 2 seg entre casillas)")
        # Inicializar timer display
        self.timer_label.config(text="Tiempo: 12.0s", fg='#27ae60')
        
    def show_game_over(self, game_state):
        """Muestra la pantalla de game over"""
        self.disable_all_inputs()
        self.instruction_label.config(text="💀 ¡Juego Terminado!")
        self.timer_label.config(text="Tiempo: --", fg='#e74c3c')
        self.calcular_y_mostrar_valor_en_dolares(game_state['score'])
        
        messagebox.showinfo(
            "Juego Terminado",
            f"¡Has perdido!\n\nNivel alcanzado: {game_state['level']}\nPuntuación final: {game_state['score']}\n\n¡Inténtalo de nuevo!"
        )
        
    def show_timeout_game_over(self, data):
        """Muestra game over por timeout"""
        self.disable_all_inputs()
        self.instruction_label.config(text="⏰ ¡Tiempo Agotado!")
        self.timer_label.config(text="Tiempo: 0.0s", fg='#e74c3c')
        
        messagebox.showwarning(
            "Tiempo Agotado",
            f"{data['message']}\n\nNivel alcanzado: {data['state']['level']}\nPuntuación final: {data['state']['score']}\n\n¡Inténtalo de nuevo!"
        )
        
    def show_victory(self, game_state):
        """Muestra la pantalla de victoria"""
        self.disable_all_inputs()
        self.instruction_label.config(text="🏆 ¡VICTORIA TOTAL!")
        self.timer_label.config(text="Tiempo: --", fg='#27ae60')
        self.calcular_y_mostrar_valor_en_dolares(game_state['score'])
        
        messagebox.showinfo(
            "¡FELICITACIONES!",
            f"¡Has completado todos los niveles!\n\nPuntuación final: {game_state['score']}\n\n¡Eres un maestro de los patrones!"
        )
        
    def on_level_completed(self):
        """Se ejecuta cuando se completa un nivel"""
        self.instruction_label.config(text="¡Nivel completado! Preparando siguiente...")
        self.timer_label.config(text="Tiempo: --", fg='#27ae60')
        
    def schedule_next_pattern(self, delay):
        """Programa mostrar el siguiente patrón después de un delay"""
        self.root.after(int(delay * 1000), self.game.show_pattern_to_player)
        
    def update_timer_display(self, remaining_time):
        """Actualiza la visualización del timer"""
        if remaining_time <= 0:
            self.timer_label.config(text="Tiempo: 0.0s", fg='#e74c3c')
        else:
            color = '#e74c3c' if remaining_time <= 3 else '#f39c12' if remaining_time <= 6 else '#27ae60'
            self.timer_label.config(text=f"Tiempo: {remaining_time:.1f}s", fg=color)
            
        # Forzar actualización de la ventana de manera segura
        try:
            self.root.update_idletasks()
        except tk.TclError:
            pass  # Evitar errores si la ventana se está cerrando
        
    # === MÉTODOS DE PRESENTACIÓN VISUAL ===
    def update_display(self, game_state):
        """Actualiza la información mostrada en pantalla"""
        self.level_label.config(text=f"Nivel: {game_state['level']}")
        self.score_label.config(text=f"Puntuación: {game_state['score']}")
        
    def flash_button(self, color):
        """Hace un flash visual en un botón"""
        if color in self.buttons:
            self.buttons[color].config(relief='sunken', bd=5)
            self.root.after(200, lambda: self.buttons[color].config(relief='raised', bd=3))
            
    def highlight_button(self, color, highlight):
        """Ilumina o apaga un botón durante la animación"""
        if color in self.buttons:
            if highlight:
                self.buttons[color].config(relief='sunken', bd=5)
            else:
                self.buttons[color].config(relief='raised', bd=3)
                
    def _animate_pattern(self, sequence, speed):
        """Ejecuta la animación del patrón (en hilo separado)"""
        time.sleep(0.5)  # Pausa inicial
        
        for color in sequence:
            # Iluminar botón
            self.root.after(0, lambda c=color: self.highlight_button(c, True))
            time.sleep(speed)
            
            # Apagar botón
            self.root.after(0, lambda c=color: self.highlight_button(c, False))
            time.sleep(speed * 0.3)
            
        # Notificar al juego que terminó la animación
        self.root.after(100, self.game.pattern_display_finished)
        
    
    def calcular_y_mostrar_valor_en_dolares(self, score):
        """Calcula y muestra el valor en dólares usando el tipo de cambio de venta del BCCR"""
        """Calcula y muestra el valor en dólares usando el tipo de cambio de venta del BCCR"""
        if score <= 0:
            messagebox.showwarning("Cálculo inválido", "⚠️ No se puede calcular: la puntuación es 0 o menor.")
            return

        try:
            if not self.correo_api or not self.token_api:
                raise ValueError("Credenciales de API no configuradas")

            bccr = TipoCambioBCCR(self.correo_api, self.token_api)
            tipo_cambio_crc = bccr.obtener_venta()

            if not tipo_cambio_crc or tipo_cambio_crc <= 0:
                raise ValueError("Tipo de cambio inválido")

            resultado_dolares = (1 / score) * 100 * tipo_cambio_crc

            mensaje = (
                f"💰 Tipo de cambio del dólar: ₡{tipo_cambio_crc:.2f}\n"
                f"💵 Operación: 1/{score} * 100 * {tipo_cambio_crc:.2f} = ${resultado_dolares:.2f} USD\n"
                f"🎯 Tu puntuación de {score} vale ${resultado_dolares:.2f} USD"
            )
            messagebox.showinfo("Resultado final", mensaje)
            guardar_mejores_resultados(score, resultado_dolares)


        except:
            # Cálculo de respaldo sin mostrar errores técnicos
            puntos_base = (1 / score) * 100
            mensaje_respaldo = (
                "⚠️ No se pudo obtener el tipo de cambio oficial.\n"
                f"💵 Cálculo de respaldo: 1/{score} * 100 = {puntos_base:.2f} puntos"
            )
            messagebox.showwarning("Cálculo de respaldo", mensaje_respaldo)

        
    # === MÉTODOS DE CONTROL DE UI ===
    def enable_color_buttons(self):
        """Habilita solo los botones de colores"""
        for button in self.buttons.values():
            button.config(state='normal')
            
    def disable_color_buttons(self):
        """Deshabilita solo los botones de colores"""
        for button in self.buttons.values():
            button.config(state='disabled')
            
    def disable_all_inputs(self):
        """Deshabilita todos los controles"""
        self.disable_color_buttons()
        
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    # Ejemplo de uso con credenciales de API
    # Reemplaza con tus credenciales reales
    correo_api = "jason.vargas.jy@gmail.com"  # Reemplaza con tu correo real
    token_api = "SANMAI01V4"           # Reemplaza con tu token real
    
    # Mostrar tipo de cambio del día antes de iniciar el juego
    print("🔄 Obteniendo tipo de cambio actual...")
    mostrar_tipo_cambio_hoy(correo_api, token_api)
    print()  # Línea en blanco para separar
    
    # Crear el juego con credenciales (opcional)
    game = PatternGameGUI(correo_api, token_api)
    # O sin credenciales: game = PatternGameGUI()
    game.run()