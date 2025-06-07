import random
import time
import threading

class PatternGame:
    def __init__(self, ui_callback=None):
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.score = 0
        self.game_over = False
        self.showing_pattern = False
        self.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan', 
                      'lime', 'magenta', 'brown', 'navy', 'olive', 'maroon', 'teal', 'silver']
        self.max_level = 10
        self.ui_callback = ui_callback
        
        # Timer variables
        self.total_time_limit = 12.0  # 12 seconds total
        self.between_clicks_limit = 2.0  # 2 seconds between clicks
        self.pattern_start_time = None
        self.last_click_time = None
        self.timer_thread = None
        self.input_enabled = False
        self.timer_stop_flag = False
        
    def start_new_game(self):
        """Inicia un nuevo juego"""
        # Reset all variables
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.score = 0
        self.game_over = False
        self.showing_pattern = False
        self.input_enabled = False
        self.stop_timers()
        
        # Generar secuencia inicial de 3 casillas
        self.generate_initial_sequence()
        
        # Notificar a la UI
        if self.ui_callback:
            self.ui_callback('game_started', self.get_game_state())
            self.ui_callback('update_display', self.get_game_state())
            # Esperar un momento antes de mostrar el patrón
            self.ui_callback('schedule_next_pattern', {'delay': 0.5})
        
    def generate_initial_sequence(self):
        """Genera la secuencia inicial con exactamente 3 casillas"""
        self.sequence = []
        for _ in range(3):  # Comenzar con exactamente 3 casillas
            new_color = random.choice(self.colors)
            self.sequence.append(new_color)
        self.player_sequence = []
        print(f"Secuencia inicial generada (Nivel {self.level}): {self.sequence}")  # Debug
        
    def generate_next_sequence(self):
        """Genera la siguiente secuencia añadiendo un color aleatorio"""
        new_color = random.choice(self.colors)
        self.sequence.append(new_color)
        self.player_sequence = []
        print(f"Nueva secuencia generada (Nivel {self.level}): {self.sequence}")  # Debug
        
    def get_current_sequence(self):
        """Retorna la secuencia actual"""
        return self.sequence.copy()
        
    def add_player_input(self, color):
        """Añade la entrada del jugador y verifica si es correcta"""
        if self.showing_pattern or self.game_over or not self.input_enabled:
            print(f"Input ignorado: showing_pattern={self.showing_pattern}, game_over={self.game_over}, input_enabled={self.input_enabled}")
            return False
        
        current_time = time.time()
        
        # Verificar tiempo entre clicks (excepto el primer click)
        if self.last_click_time is not None:
            time_between_clicks = current_time - self.last_click_time
            if time_between_clicks > self.between_clicks_limit:
                self.timeout_game_over("¡Tiempo agotado entre casillas! (Máximo 2 segundos)")
                return False
        
        # Verificar tiempo total
        if self.pattern_start_time is not None:
            total_time = current_time - self.pattern_start_time
            if total_time > self.total_time_limit:
                self.timeout_game_over("¡Tiempo total agotado! (Máximo 12 segundos)")
                return False
        
        self.last_click_time = current_time
        self.player_sequence.append(color)
        print(f"Player input: {color}, secuencia actual: {self.player_sequence}")  # Debug
        
        # Notificar tiempo restante a la UI
        if self.ui_callback and self.pattern_start_time:
            remaining_time = max(0, self.total_time_limit - (current_time - self.pattern_start_time))
            self.ui_callback('time_update', {'remaining_time': remaining_time})
        
        # Verificar si la entrada es correcta hasta ahora
        if not self.is_sequence_correct_so_far():
            print("Secuencia incorrecta!")  # Debug
            self.game_over = True
            self.stop_timers()
            if self.ui_callback:
                self.ui_callback('game_over', self.get_game_state())
            return False
            
        # Verificar si el jugador completó la secuencia
        if len(self.player_sequence) == len(self.sequence):
            print("¡Secuencia completada correctamente!")  # Debug
            self.stop_timers()
            self.input_enabled = False
            self.score += self.level * 10
            self.level += 1
            
            if self.level > self.max_level:
                # Jugador ganó el juego completo
                if self.ui_callback:
                    self.ui_callback('victory', self.get_game_state())
                return True
                
            # Generar siguiente secuencia
            self.generate_next_sequence()
            if self.ui_callback:
                self.ui_callback('update_display', self.get_game_state())
                self.ui_callback('level_completed', self.get_game_state())
            
            # Mostrar la siguiente secuencia después de un breve delay
            if self.ui_callback:
                self.ui_callback('schedule_next_pattern', {'delay': 2.0})
            
        return True
        
    def timeout_game_over(self, message):
        """Termina el juego por timeout"""
        print(f"Timeout game over: {message}")  # Debug
        self.game_over = True
        self.input_enabled = False
        self.stop_timers()
        if self.ui_callback:
            self.ui_callback('timeout_game_over', {'message': message, 'state': self.get_game_state()})
        
    def is_sequence_correct_so_far(self):
        """Verifica si la secuencia del jugador es correcta hasta el momento"""
        for i in range(len(self.player_sequence)):
            if self.player_sequence[i] != self.sequence[i]:
                return False
        return True
        
    def get_game_state(self):
        """Retorna el estado actual del juego"""
        remaining_time = 0
        if self.pattern_start_time and self.input_enabled and not self.game_over:
            remaining_time = max(0, self.total_time_limit - (time.time() - self.pattern_start_time))
            
        return {
            'level': self.level,
            'score': self.score,
            'game_over': self.game_over,
            'showing_pattern': self.showing_pattern,
            'sequence_length': len(self.sequence),
            'player_progress': len(self.player_sequence),
            'won_game': self.level > self.max_level and not self.game_over,
            'input_enabled': self.input_enabled,
            'remaining_time': remaining_time
        }
        
    def set_showing_pattern(self, showing):
        """Establece si se está mostrando el patrón"""
        self.showing_pattern = showing
        
    def get_pattern_display_speed(self):
        """Retorna la velocidad de visualización basada en el nivel"""
        base_speed = 1.0
        speed_increase = min(self.level * 0.1, 0.5)
        return max(base_speed - speed_increase, 0.3)
        
    def show_pattern_to_player(self):
        """Inicia el proceso de mostrar el patrón al jugador"""
        if self.showing_pattern or self.game_over:
            print(f"No se puede mostrar patrón: showing_pattern={self.showing_pattern}, game_over={self.game_over}")
            return
            
        print(f"Iniciando mostrar patrón: {self.sequence}")  # Debug
        self.showing_pattern = True
        self.input_enabled = False
        self.stop_timers()
        
        if self.ui_callback:
            self.ui_callback('start_pattern_display', {
                'sequence': self.get_current_sequence(),
                'speed': self.get_pattern_display_speed()
            })
    
    def pattern_display_finished(self):
        """La UI llama a este método cuando termina de mostrar el patrón"""
        print("Patrón mostrado completamente, habilitando input")  # Debug
        self.showing_pattern = False
        self.input_enabled = True
        self.start_timers()
        
        if self.ui_callback:
            self.ui_callback('enable_player_input', self.get_game_state())
            
    def start_timers(self):
        """Inicia los timers para el jugador"""
        print("Iniciando timers")  # Debug
        self.pattern_start_time = time.time()
        self.last_click_time = None
        self.timer_stop_flag = False
        
        # Iniciar timer en hilo separado para verificar tiempo total
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_stop_flag = True
            self.timer_thread.join(timeout=0.5)
            
        self.timer_thread = threading.Thread(target=self._timer_worker, daemon=True)
        self.timer_thread.start()
        
    def _timer_worker(self):
        """Worker thread para el timer"""
        start_time = time.time()
        print(f"Timer worker iniciado a las {start_time}")  # Debug
        
        while self.input_enabled and not self.game_over and not self.timer_stop_flag:
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = self.total_time_limit - elapsed
            
            # Actualizar UI cada 100ms
            if self.ui_callback and remaining > 0:
                self.ui_callback('time_update', {'remaining_time': remaining})
            
            if remaining <= 0:
                print("Timer worker: tiempo agotado")  # Debug
                self.timeout_game_over("¡Tiempo total agotado! (Máximo 12 segundos)")
                break
                
            time.sleep(0.1)  # Update every 100ms
            
        print("Timer worker terminado")  # Debug
            
    def stop_timers(self):
        """Detiene todos los timers"""
        print("Deteniendo timers")  # Debug
        self.timer_stop_flag = True
        self.input_enabled = False
        self.pattern_start_time = None
        self.last_click_time = None
        
        # Asegurar que el hilo del timer se detenga
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=0.5)
        
    def request_pattern_display(self):
        """El jugador solicita ver el patrón nuevamente"""
        print("Solicitando mostrar patrón")  # Debug
        self.show_pattern_to_player()
        
    def can_show_pattern(self):
        """Verifica si se puede mostrar el patrón"""
        can_show = not self.showing_pattern and not self.game_over and not self.input_enabled
        print(f"Can show pattern: {can_show} (showing={self.showing_pattern}, game_over={self.game_over}, input_enabled={self.input_enabled})")  # Debug
        return can_show
        
    def reset_player_sequence(self):
        """Reinicia la secuencia del jugador"""
        self.player_sequence = []