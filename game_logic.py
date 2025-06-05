import random
import time

class PatternGame:
    def __init__(self, ui_callback=None):
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.score = 0
        self.game_over = False
        self.showing_pattern = False
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.max_level = 20
        self.ui_callback = ui_callback  # Callback para comunicarse con la UI
        
    def start_new_game(self):
        """Inicia un nuevo juego"""
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.score = 0
        self.game_over = False
        self.showing_pattern = False
        self.generate_next_sequence()
        
        # Notificar a la UI
        if self.ui_callback:
            self.ui_callback('game_started', self.get_game_state())
            self.ui_callback('update_display', self.get_game_state())
            # Iniciar automáticamente la primera secuencia
            self.show_pattern_to_player()
        
    def generate_next_sequence(self):
        """Genera la siguiente secuencia añadiendo un color aleatorio"""
        new_color = random.choice(self.colors)
        self.sequence.append(new_color)
        self.player_sequence = []
        
    def get_current_sequence(self):
        """Retorna la secuencia actual"""
        return self.sequence.copy()
        
    def add_player_input(self, color):
        """Añade la entrada del jugador y verifica si es correcta"""
        if self.showing_pattern or self.game_over:
            return False
            
        self.player_sequence.append(color)
        
        # Verificar si la entrada es correcta hasta ahora
        if not self.is_sequence_correct_so_far():
            self.game_over = True
            if self.ui_callback:
                self.ui_callback('game_over', self.get_game_state())
            return False
            
        # Verificar si el jugador completó la secuencia
        if len(self.player_sequence) == len(self.sequence):
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
            self.show_pattern_to_player()
            
        return True
        
    def is_sequence_correct_so_far(self):
        """Verifica si la secuencia del jugador es correcta hasta el momento"""
        for i in range(len(self.player_sequence)):
            if self.player_sequence[i] != self.sequence[i]:
                return False
        return True
        
    def get_game_state(self):
        """Retorna el estado actual del juego"""
        return {
            'level': self.level,
            'score': self.score,
            'game_over': self.game_over,
            'showing_pattern': self.showing_pattern,
            'sequence_length': len(self.sequence),
            'player_progress': len(self.player_sequence),
            'won_game': self.level > self.max_level and not self.game_over
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
            return
            
        self.showing_pattern = True
        if self.ui_callback:
            self.ui_callback('start_pattern_display', {
                'sequence': self.get_current_sequence(),
                'speed': self.get_pattern_display_speed()
            })
    
    def pattern_display_finished(self):
        """La UI llama a este método cuando termina de mostrar el patrón"""
        self.showing_pattern = False
        if self.ui_callback:
            self.ui_callback('enable_player_input', self.get_game_state())
    
    def request_pattern_display(self):
        """El jugador solicita ver el patrón nuevamente"""
        self.show_pattern_to_player()
        
    def can_show_pattern(self):
        """Verifica si se puede mostrar el patrón"""
        return not self.showing_pattern and not self.game_over