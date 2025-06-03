import tkinter as tk
from tkinter import messagebox
import threading
import time
from game_logic import PatternGame

class PatternGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juego de Patrones")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
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
            self.enable_player_input()
        elif event_type == 'game_over':
            self.show_game_over(data)
        elif event_type == 'victory':
            self.show_victory(data)
        elif event_type == 'level_completed':
            self.on_level_completed()
            
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Título
        title_label = tk.Label(
            self.root, 
            text="🎮 JUEGO DE PATRONES 🎮", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50', 
            fg='white'
        )
        title_label.pack(pady=20)
        
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
        self.level_label.pack(side=tk.LEFT, padx=20)
        
        self.score_label = tk.Label(
            self.info_frame, 
            text="Puntuación: 0", 
            font=('Arial', 14),
            bg='#2c3e50', 
            fg='white'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        # Frame de instrucciones
        self.instruction_label = tk.Label(
            self.root, 
            text="Presiona 'Nuevo Juego' para comenzar", 
            font=('Arial', 12),
            bg='#2c3e50', 
            fg='#ecf0f1'
        )
        self.instruction_label.pack(pady=10)
        
        # Frame de botones de colores
        self.game_frame = tk.Frame(self.root, bg='#2c3e50')
        self.game_frame.pack(pady=30)
        
        # Configuración de colores y posiciones
        color_config = {
            'red': {'row': 0, 'col': 0, 'bg': '#e74c3c', 'active_bg': '#ff6b6b'},
            'blue': {'row': 0, 'col': 1, 'bg': '#3498db', 'active_bg': '#5dade2'},
            'green': {'row': 1, 'col': 0, 'bg': '#2ecc71', 'active_bg': '#58d68d'},
            'yellow': {'row': 1, 'col': 1, 'bg': '#f1c40f', 'active_bg': '#f7dc6f'}
        }
        
        # Crear botones de colores
        for color, config in color_config.items():
            btn = tk.Button(
                self.game_frame,
                width=15,
                height=8,
                bg=config['bg'],
                activebackground=config['active_bg'],
                relief='raised',
                bd=3,
                command=lambda c=color: self.on_color_button_clicked(c),
                state='disabled'
            )
            btn.grid(row=config['row'], column=config['col'], padx=10, pady=10)
            self.buttons[color] = btn
            
        # Frame de controles
        self.control_frame = tk.Frame(self.root, bg='#2c3e50')
        self.control_frame.pack(pady=20)
        
        self.new_game_btn = tk.Button(
            self.control_frame,
            text="🎲 Nuevo Juego",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.on_new_game_clicked
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=10)
        
        self.show_pattern_btn = tk.Button(
            self.control_frame,
            text="👁️ Ver Patrón",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.on_show_pattern_clicked,
            state='disabled'
        )
        self.show_pattern_btn.pack(side=tk.LEFT, padx=10)
        
    # === MANEJADORES DE EVENTOS DE UI ===
    def on_new_game_clicked(self):
        """Se ejecuta cuando se presiona el botón de nuevo juego"""
        self.game.start_new_game()
        
    def on_show_pattern_clicked(self):
        """Se ejecuta cuando se presiona el botón de ver patrón"""
        if self.game.can_show_pattern():
            self.game.request_pattern_display()
            
    def on_color_button_clicked(self, color):
        """Se ejecuta cuando se presiona un botón de color"""
        # Efecto visual inmediato
        self.flash_button(color)
        # Enviar entrada al juego
        self.game.add_player_input(color)
        
    # === MANEJADORES DE EVENTOS DEL JUEGO ===
    def on_game_started(self, game_state):
        """Se ejecuta cuando el juego inicia"""
        self.instruction_label.config(text="¡Observa el patrón y repítelo!")
        self.show_pattern_btn.config(state='normal')
        
    def start_pattern_animation(self, data):
        """Inicia la animación del patrón"""
        self.disable_all_inputs()
        self.instruction_label.config(text="¡Observa atentamente el patrón!")
        
        # Ejecutar animación en hilo separado
        threading.Thread(
            target=self._animate_pattern, 
            args=(data['sequence'], data['speed']), 
            daemon=True
        ).start()
        
    def enable_player_input(self):
        """Habilita la entrada del jugador"""
        self.enable_color_buttons()
        self.show_pattern_btn.config(state='normal')
        self.instruction_label.config(text="¡Ahora repite el patrón!")
        
    def show_game_over(self, game_state):
        """Muestra la pantalla de game over"""
        self.disable_all_inputs()
        self.instruction_label.config(text="💀 ¡Juego Terminado!")
        
        messagebox.showinfo(
            "Juego Terminado",
            f"¡Has perdido!\n\nNivel alcanzado: {game_state['level']}\nPuntuación final: {game_state['score']}\n\n¡Inténtalo de nuevo!"
        )
        
    def show_victory(self, game_state):
        """Muestra la pantalla de victoria"""
        self.disable_all_inputs()
        self.instruction_label.config(text="🏆 ¡VICTORIA TOTAL!")
        
        messagebox.showinfo(
            "¡FELICITACIONES!",
            f"¡Has completado todos los niveles!\n\nPuntuación final: {game_state['score']}\n\n¡Eres un maestro de los patrones!"
        )
        
    def on_level_completed(self):
        """Se ejecuta cuando se completa un nivel"""
        self.instruction_label.config(text="¡Nivel completado! Preparando siguiente...")
        
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
        self.root.after(0, self.game.pattern_display_finished)
        
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
        self.show_pattern_btn.config(state='disabled')
        
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    game = PatternGameGUI()
    game.run()