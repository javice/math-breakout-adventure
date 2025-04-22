import pygame
import random
import os
import numpy as np
import json
import time
from datetime import datetime

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4

class MathBreakout:
    def __init__(self):
        self.bricks = None
        self.last_problem_time = None
        self.problem_start_time = None
        self.ball_speed_y = None
        self.ball_speed_x = None
        self.base_ball_speed = None
        self.ball = None
        self.paddle = None
        self.lives = None
        self.score = None
        self.level = None
        self.menu_select_sound = None
        self.menu_move_sound = None
        self.level_complete_sound = None
        self.game_over_sound = None
        self.wrong_answer_sound = None
        self.brick_hit_sound = None
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Math Breakout Adventure")
        self.clock = pygame.time.Clock()

        # Cargar sonidos
        self.load_sounds()

        # Cargar fuentes
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Cargar fondo
        self.background = self.create_background()

        # Game state
        self.game_state = MENU

        # Puntuaciones altas
        self.high_scores = self.load_high_scores()

        # Inicializar juego
        self.reset_game(1)

    def load_sounds(self):
        try:
            self.brick_hit_sound = pygame.mixer.Sound(os.path.join('sounds', 'brick_hit.wav'))
            self.wrong_answer_sound = pygame.mixer.Sound(os.path.join('sounds', 'wrong_answer.wav'))
            self.game_over_sound = pygame.mixer.Sound(os.path.join('sounds', 'game_over.wav'))
            self.level_complete_sound = pygame.mixer.Sound(os.path.join('sounds', 'level_complete.wav'))
            self.menu_move_sound = pygame.mixer.Sound(os.path.join('sounds', 'menu_move.wav'))
            self.menu_select_sound = pygame.mixer.Sound(os.path.join('sounds', 'menu_select.wav'))
        except Exception as e:
            print(f"Error cargando sonidos: {e}")
            # Fallback a generación básica de sonido
            sample_rate = 44100
            duration = 1  # 1 segundo
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

            # Crear diferentes sonidos con frecuencias distintas
            brick_wave = 0.5 * np.sin(2 * np.pi * 440 * t)
            wrong_wave = 0.5 * np.sin(2 * np.pi * 220 * t)
            game_over_wave = 0.5 * np.sin(2 * np.pi * 110 * t)
            level_complete_wave = 0.5 * np.sin(2 * np.pi * 880 * t)
            menu_move_wave = 0.3 * np.sin(2 * np.pi * 660 * t)
            menu_select_wave = 0.3 * np.sin(2 * np.pi * 770 * t)

            # Convertir a estéreo
            brick_wave = np.tile(brick_wave, (2, 1)).T
            wrong_wave = np.tile(wrong_wave, (2, 1)).T
            game_over_wave = np.tile(game_over_wave, (2, 1)).T
            level_complete_wave = np.tile(level_complete_wave, (2, 1)).T
            menu_move_wave = np.tile(menu_move_wave, (2, 1)).T
            menu_select_wave = np.tile(menu_select_wave, (2, 1)).T

            # Crear sonidos
            self.brick_hit_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(brick_wave))
            self.wrong_answer_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(wrong_wave))
            self.game_over_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(game_over_wave))
            self.level_complete_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(level_complete_wave))
            self.menu_move_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(menu_move_wave))
            self.menu_select_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(menu_select_wave))

    def create_background(self):
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(BLACK)

        # Añadir efecto de estrellas
        for _ in range(200):  # Más estrellas para mejor efecto
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.random() * 3  # Tamaños más variados

            # Colores aleatorios para algunas estrellas
            colors = [WHITE, (200, 200, 255), (255, 255, 200), (200, 255, 255)]
            color = random.choice(colors)

            pygame.draw.circle(background, color, (x, y), size)

        return background

    def load_high_scores(self):
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_high_scores(self):
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)

    def add_high_score(self, score):
        date = datetime.now().strftime("%d/%m/%Y")

        # Crear entrada de puntuación
        score_entry = {"score": score, "level": self.level, "date": date}

        # Insertar en orden
        self.high_scores.append(score_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)

        # Mantener solo los 10 mejores
        self.high_scores = self.high_scores[:10]

        # Guardar
        self.save_high_scores()

    def reset_game(self, level):
        self.level = level
        self.score = 0 if level == 1 else self.score  # Mantener puntuación al cambiar de nivel
        self.lives = 6
        self.paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
                                  SCREEN_HEIGHT - 50,
                                  PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS,
                                SCREEN_HEIGHT // 2 - BALL_RADIUS,
                                BALL_RADIUS * 2, BALL_RADIUS * 2)

        # Aumentar velocidad de la bola con cada nivel
        self.base_ball_speed = 5 + (self.level * 0.5)
        self.ball_speed_x = self.base_ball_speed
        self.ball_speed_y = -self.base_ball_speed

        # Variables para el tiempo de respuesta
        self.problem_start_time = 0
        self.last_problem_time = 0

        # Estado de juego
        self.game_state = PLAYING

        self.create_bricks()

    def create_bricks(self):
        self.bricks = []
        # Más colores para mayor variedad
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, CYAN]

        # Más ladrillos para niveles más altos
        rows = min(5 + self.level, 12)  # Límite de 12 filas para que no sea imposible

        for row in range(rows):
            for col in range(10):
                brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 50,
                                    row * (BRICK_HEIGHT + 5) + 50,
                                    BRICK_WIDTH, BRICK_HEIGHT)
                # Asignar diferentes colores según fila y nivel
                brick_color = colors[row % len(colors)]
                self.bricks.append((brick, brick_color))

    def generate_math_problem(self):
        # Aumentar complejidad del problema con el nivel
        operators = ['+', '-', '*']
        if self.level > 3:
            operators.append('/')

        operator = random.choice(operators)

        if operator == '+':
            a = random.randint(1, 20 + self.level * 5)
            b = random.randint(1, 20 + self.level * 5)
            problem = f"{a} + {b} = ?"
            answer = a + b
        elif operator == '-':
            a = random.randint(10, 50 + self.level * 10)
            b = random.randint(1, a)
            problem = f"{a} - {b} = ?"
            answer = a - b
        elif operator == '*':
            a = random.randint(1, 10 + self.level)
            b = random.randint(1, 10 + self.level)
            problem = f"{a} * {b} = ?"
            answer = a * b
        else:  # División para niveles superiores
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            problem = f"{a} ÷ {b} = ?"
            answer = a // b

        self.problem_start_time = time.time()
        return problem, answer

    def show_math_problem(self, problem):
        # Guardar pantalla original
        global user_answer
        original_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        original_surface.blit(self.screen, (0, 0))

        # Crear una superficie para el cuadro de diálogo
        dialog_width, dialog_height = 500, 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2

        # Dibujar cuadro de diálogo
        input_box = pygame.Rect(dialog_x + 150, dialog_y + 200, 200, 50)
        color_inactive = BLUE
        color_active = GREEN
        color = color_inactive
        active = True  # Activo por defecto
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            try:
                                user_answer = int(text)
                                done = True
                            except ValueError:
                                text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            # Cancelar diálogo
                            return None
                        else:
                            # Solo permitir números
                            if event.unicode.isdigit() or (event.unicode == '-' and not text):
                                text += event.unicode

            # Volver a dibujar la pantalla original
            self.screen.blit(original_surface, (0, 0))

            # Dibujar panel semitransparente
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((0, 0, 0, 200))  # Negro semitransparente
            self.screen.blit(dialog_surface, (dialog_x, dialog_y))

            # Dibujar borde
            pygame.draw.rect(self.screen, WHITE,
                             (dialog_x, dialog_y, dialog_width, dialog_height), 2)

            # Mostrar problema
            title_text = self.title_font.render("Desafío Matemático", True, WHITE)
            problem_txt = self.font.render(problem, True, WHITE)
            instruction_txt = self.small_font.render("Escribe la respuesta y presiona Enter", True, WHITE)

            self.screen.blit(title_text, (dialog_x + (dialog_width - title_text.get_width()) // 2, dialog_y + 30))
            self.screen.blit(problem_txt, (dialog_x + (dialog_width - problem_txt.get_width()) // 2, dialog_y + 100))
            self.screen.blit(instruction_txt, (dialog_x + (dialog_width - instruction_txt.get_width()) // 2, dialog_y + 150))

            # Dibujar caja de entrada
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Mostrar tiempo transcurrido
            elapsed = time.time() - self.problem_start_time
            timer_text = self.small_font.render(f"Tiempo: {elapsed:.1f}s", True, WHITE)
            self.screen.blit(timer_text, (dialog_x + dialog_width - 150, dialog_y + dialog_height - 40))

            pygame.display.flip()
            self.clock.tick(30)

        self.last_problem_time = time.time() - self.problem_start_time
        return user_answer

    def show_game_over(self):
        self.game_state = GAME_OVER
        self.add_high_score(self.score)

        # Sonido de fin de juego
        self.game_over_sound.play()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparente
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render("¡GAME OVER!", True, RED)
        score_text = self.font.render(f"Puntuación: {self.score}", True, WHITE)
        level_text = self.font.render(f"Nivel alcanzado: {self.level}", True, WHITE)
        continue_text = self.font.render("Presiona ESPACIO para volver al menú", True, WHITE)

        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        # Esperar a que el jugador presione espacio
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        self.game_state = MENU
            self.clock.tick(30)

    def show_level_completed(self):
        self.game_state = LEVEL_COMPLETE

        # Sonido de nivel completado
        self.level_complete_sound.play()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparente
        self.screen.blit(overlay, (0, 0))

        level_text = self.title_font.render(f"¡NIVEL {self.level} COMPLETADO!", True, GREEN)
        score_text = self.font.render(f"Puntuación actual: {self.score}", True, WHITE)
        next_level_text = self.font.render(f"Preparando nivel {self.level + 1}...", True, WHITE)
        continue_text = self.font.render("Presiona ESPACIO para continuar", True, WHITE)

        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2,
                                           SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        # Esperar a que el jugador presione espacio
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        self.level += 1
                        self.reset_game(self.level)
            self.clock.tick(30)

    def show_pause_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparente
        self.screen.blit(overlay, (0, 0))

        pause_text = self.title_font.render("PAUSA", True, WHITE)
        continue_text = self.font.render("Presiona ESC para continuar", True, WHITE)
        quit_text = self.font.render("Presiona Q para salir al menú", True, WHITE)

        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def show_main_menu(self):
        self.screen.blit(self.background, (0, 0))

        # Título
        title_text = self.title_font.render("MATH BREAKOUT ADVENTURE", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Opciones de menú
        menu_items = ["Jugar", "Puntuaciones Altas", "Instrucciones", "Salir"]
        menu_positions = []

        for i, item in enumerate(menu_items):
            text = self.font.render(item, True, WHITE)
            y_pos = 300 + i * 60
            x_pos = SCREEN_WIDTH // 2 - text.get_width() // 2

            # Almacenar posición para detección de clics
            menu_positions.append((item, pygame.Rect(x_pos - 10, y_pos - 10,
                                                     text.get_width() + 20, text.get_height() + 20)))

            # Dibujar texto
            self.screen.blit(text, (x_pos, y_pos))

        # Versión en la esquina
        version_text = self.small_font.render("v1.2.0", True, WHITE)
        self.screen.blit(version_text, (SCREEN_WIDTH - version_text.get_width() - 10,
                                        SCREEN_HEIGHT - version_text.get_height() - 10))

        pygame.display.flip()

        # Control de menú
        selected = None

        while self.game_state == MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Manejar clics de ratón
                if event.type == pygame.MOUSEMOTION:
                    for item, rect in menu_positions:
                        if rect.collidepoint(event.pos):
                            if selected != item:
                                selected = item
                                self.menu_move_sound.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item, rect in menu_positions:
                        if rect.collidepoint(event.pos):
                            self.menu_select_sound.play()
                            self.handle_menu_selection(item)

                # Manejar teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Mover selección hacia arriba
                        current_idx = menu_items.index(selected) if selected in menu_items else 0
                        new_idx = (current_idx - 1) % len(menu_items)
                        selected = menu_items[new_idx]
                        self.menu_move_sound.play()

                    elif event.key == pygame.K_DOWN:
                        # Mover selección hacia abajo
                        current_idx = menu_items.index(selected) if selected in menu_items else 0
                        new_idx = (current_idx + 1) % len(menu_items)
                        selected = menu_items[new_idx]
                        self.menu_move_sound.play()

                    elif event.key == pygame.K_RETURN:
                        # Seleccionar opción
                        if selected:
                            self.menu_select_sound.play()
                            self.handle_menu_selection(selected)

            # Volver a dibujar el menú con la selección resaltada
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            for i, (item, rect) in enumerate(menu_positions):
                # Resaltar la opción seleccionada
                if item == selected:
                    pygame.draw.rect(self.screen, BLUE, rect, border_radius=5)
                    text = self.font.render(item, True, YELLOW)
                else:
                    text = self.font.render(item, True, WHITE)

                self.screen.blit(text, (rect.x + 10, rect.y + 10))

            self.screen.blit(version_text, (SCREEN_WIDTH - version_text.get_width() - 10,
                                            SCREEN_HEIGHT - version_text.get_height() - 10))

            pygame.display.flip()
            self.clock.tick(30)

    def handle_menu_selection(self, selected):
        if selected == "Jugar":
            self.reset_game(1)
            self.game_state = PLAYING
        elif selected == "Puntuaciones Altas":
            self.show_high_scores()
        elif selected == "Instrucciones":
            self.show_instructions()
        elif selected == "Salir":
            pygame.quit()
            exit()

    def show_high_scores(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            title_text = self.title_font.render("MEJORES PUNTUACIONES", True, YELLOW)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            if not self.high_scores:
                no_scores = self.font.render("No hay puntuaciones guardadas", True, WHITE)
                self.screen.blit(no_scores, (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, 300))
            else:
                # Encabezado
                header_y = 200
                pos_header = self.font.render("#", True, CYAN)
                score_header = self.font.render("Puntuación", True, CYAN)
                level_header = self.font.render("Nivel", True, CYAN)
                date_header = self.font.render("Fecha", True, CYAN)

                self.screen.blit(pos_header, (200, header_y))
                self.screen.blit(score_header, (300, header_y))
                self.screen.blit(level_header, (500, header_y))
                self.screen.blit(date_header, (650, header_y))

                # Lista de puntuaciones
                for i, entry in enumerate(self.high_scores):
                    y_pos = 250 + i * 40

                    pos_text = self.font.render(f"{i+1}.", True, WHITE)
                    score_text = self.font.render(f"{entry['score']}", True, WHITE)
                    level_text = self.font.render(f"{entry['level']}", True, WHITE)
                    date_text = self.font.render(f"{entry['date']}", True, WHITE)

                    self.screen.blit(pos_text, (200, y_pos))
                    self.screen.blit(score_text, (300, y_pos))
                    self.screen.blit(level_text, (500, y_pos))
                    self.screen.blit(date_text, (650, y_pos))

            back_text = self.font.render("Presiona ESC para volver", True, WHITE)
            self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 650))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.game_state = MENU

            self.clock.tick(30)

    def show_instructions(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            title_text = self.title_font.render("INSTRUCCIONES", True, YELLOW)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            instructions = [
                "- Usa las FLECHAS IZQUIERDA y DERECHA para mover la paleta",
                "- Golpea los ladrillos con la bola para destruirlos",
                "- Cuando golpeas un ladrillo, deberás resolver un problema matemático",
                "- Si respondes correctamente, el ladrillo desaparece y ganas puntos",
                "- Si fallas, pierdes una vida",
                "- Perderás una vida si la bola cae por debajo de la pantalla",
                "- El juego termina cuando pierdes todas tus vidas",
                "- Completar un nivel aumenta la dificultad",
                "- Presiona ESC durante el juego para pausar",
                "- ¡Diviértete y mejora tus habilidades matemáticas!"
            ]

            for i, line in enumerate(instructions):
                instruction_text = self.font.render(line, True, WHITE)
                self.screen.blit(instruction_text, (150, 200 + i * 40))

            back_text = self.font.render("Presiona ESC para volver", True, WHITE)
            self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 650))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.game_state = MENU

            self.clock.tick(30)

    def calculate_score_for_answer(self):
        # Dar más puntos por respuestas rápidas
        base_score = 100
        time_bonus = max(0, 5 - self.last_problem_time) * 20  # 20 puntos por cada segundo bajo 5
        level_bonus = self.level * 10  # 10 puntos adicionales por nivel
        return int(base_score + time_bonus + level_bonus)

    def run(self):
        running = True
        self.game_state = MENU

        while running:
            if self.game_state == MENU:
                self.show_main_menu()


            elif self.game_state == PLAYING:
                # Manejar eventos
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = PAUSED

                # Controlar la paleta
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.paddle.left > 0:
                    self.paddle.x -= 10
                if keys[pygame.K_RIGHT] and self.paddle.right < SCREEN_WIDTH:
                    self.paddle.x += 10

                # Movimiento de la pelota
                self.ball.x += self.ball_speed_x
                self.ball.y += self.ball_speed_y

                # Colisión de la pelota con las paredes
                if self.ball.left <= 0:
                    self.ball.left = 0
                    self.ball_speed_x *= -1
                elif self.ball.right >= SCREEN_WIDTH:
                    self.ball.right = SCREEN_WIDTH
                    self.ball_speed_x *= -1
                if self.ball.top <= 0:
                    self.ball.top = 0
                    self.ball_speed_y *= -1

                # Colisión con la paleta
                if self.ball.colliderect(self.paddle):
                    # Cambiar dirección según dónde golpee la paleta (para dar más control)
                    relative_intersect_x = (self.paddle.x + (PADDLE_WIDTH / 2)) - self.ball.x
                    normalized_relative_intersect_x = relative_intersect_x / (PADDLE_WIDTH / 2)
                    bounce_angle = normalized_relative_intersect_x * (np.pi / 3)  # Máximo 60 grados

                    # Calcular nueva dirección
                    self.ball_speed_x = self.base_ball_speed * -np.sin(bounce_angle)
                    self.ball_speed_y = self.base_ball_speed * -np.cos(bounce_angle)

                    # Asegurar que la bola no quede atrapada en la paleta
                    self.ball.bottom = self.paddle.top - 1

                # Colisión con los ladrillos
                for brick_data in self.bricks[:]:
                    brick, color = brick_data
                    if self.ball.colliderect(brick):
                        # Detectar lado de colisión de manera más precisa
                        # Calcular distancias a cada lado del ladrillo
                        left_dist = abs(self.ball.right - brick.left)
                        right_dist = abs(self.ball.left - brick.right)
                        top_dist = abs(self.ball.bottom - brick.top)
                        bottom_dist = abs(self.ball.top - brick.bottom)

                        # Encontrar la distancia mínima para determinar el lado de colisión
                        min_dist = min(left_dist, right_dist, top_dist, bottom_dist)

                        # Ajustar posición y velocidad según el lado de colisión
                        if min_dist == left_dist:
                            self.ball.right = brick.left - 1
                            self.ball_speed_x = -abs(self.ball_speed_x)
                        elif min_dist == right_dist:
                            self.ball.left = brick.right + 1
                            self.ball_speed_x = abs(self.ball_speed_x)
                        elif min_dist == top_dist:
                            self.ball.bottom = brick.top - 1
                            self.ball_speed_y = -abs(self.ball_speed_y)
                        elif min_dist == bottom_dist:
                            self.ball.top = brick.bottom + 1
                            self.ball_speed_y = abs(self.ball_speed_y)

                        # Generar problema matemático
                        problem, correct_answer = self.generate_math_problem()
                        user_answer = self.show_math_problem(problem)

                        # Si el usuario cancela, salir sin destruir el ladrillo
                        if user_answer is None:
                            continue

                        if user_answer == correct_answer:
                            self.brick_hit_sound.play()
                            # Puntuación basada en el tiempo de respuesta
                            points = self.calculate_score_for_answer()
                            self.score += points

                            # Mostrar puntos ganados
                            self.show_points_popup(points, brick.centerx, brick.centery)

                            # Eliminar ladrillo
                            self.bricks.remove(brick_data)
                        else:
                            self.wrong_answer_sound.play()
                            self.lives -= 1
                            if self.lives <= 0:
                                self.show_game_over()
                            else:
                                # Mostrar mensaje de respuesta incorrecta
                                self.show_wrong_answer_popup(correct_answer)

                                # Mover la bola de nuevo a la posición inicial
                                self.ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                                self.ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS

                        # Mantener la velocidad progresiva
                        ball_speed_base = self.base_ball_speed
                        ball_speed_direction_x = 1 if self.ball_speed_x > 0 else -1
                        ball_speed_direction_y = 1 if self.ball_speed_y > 0 else -1
                        self.ball_speed_x = ball_speed_base * ball_speed_direction_x
                        self.ball_speed_y = -abs(ball_speed_base * ball_speed_direction_y)
                        break  # Salir del bucle después de procesar una colisión

                # Dibujo
                self.screen.blit(self.background, (0, 0))
                pygame.draw.rect(self.screen, BLUE, self.paddle)
                pygame.draw.ellipse(self.screen, WHITE, self.ball)

                # Dibujar ladrillos con colores
                for brick, color in self.bricks:
                    pygame.draw.rect(self.screen, color, brick)
                    # Añadir borde para mejor visualización
                    pygame.draw.rect(self.screen, WHITE, brick, 1)

                # Mostrar puntuación y vidas
                score_text = self.font.render(f"Puntuación: {self.score}", True, WHITE)
                lives_text = self.font.render(f"Vidas: {self.lives}", True, WHITE)
                level_text = self.font.render(f"Nivel: {self.level}", True, WHITE)

                self.screen.blit(score_text, (10, 10))
                self.screen.blit(lives_text, (10, 50))
                self.screen.blit(level_text, (10, 90))

                # Condiciones de game over
                if self.ball.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.show_game_over()
                    else:
                        # Mostrar mensaje de pérdida de vida
                        self.show_life_lost_popup()

                        # Mover la bola de nuevo a la posición inicial
                        self.ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                        self.ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS

                        # Resetear la velocidad de la bola para dar tiempo al jugador
                        self.ball_speed_x = self.base_ball_speed * (1 if random.random() > 0.5 else -1)
                        self.ball_speed_y = -self.base_ball_speed

                # Nivel completado
                if not self.bricks:
                    self.show_level_completed()

                pygame.display.flip()
                self.clock.tick(60)

            elif self.game_state == PAUSED:
                # Mostrar menú de pausa
                self.show_pause_menu()

                # Manejar eventos durante la pausa
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = PLAYING
                        elif event.key == pygame.K_q:
                            self.game_state = MENU

                self.clock.tick(30)

            elif self.game_state == GAME_OVER:
                # Estado manejado por show_game_over
                pass

            elif self.game_state == LEVEL_COMPLETE:
                # Estado manejado por show_level_completed
                pass

    def show_points_popup(self, points, x, y):
        # Añadir una animación pequeña para los puntos ganados
        points_text = self.font.render(f"+{points}", True, GREEN)
        self.screen.blit(points_text, (x - points_text.get_width() // 2, y))
        pygame.display.update()
        pygame.time.wait(200)  # Mostrar brevemente

    def show_wrong_answer_popup(self, correct_answer):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 100))  # Rojo semitransparente
        self.screen.blit(overlay, (0, 0))

        wrong_text = self.font.render("¡Respuesta Incorrecta!", True, WHITE)
        correct_text = self.font.render(f"La respuesta correcta era: {correct_answer}", True, WHITE)
        continue_text = self.font.render("Continuar...", True, WHITE)

        self.screen.blit(wrong_text, (SCREEN_WIDTH // 2 - wrong_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(correct_text, (SCREEN_WIDTH // 2 - correct_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        pygame.time.wait(2000)  # Esperar 2 segundos

    def show_life_lost_popup(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 100))  # Rojo semitransparente
        self.screen.blit(overlay, (0, 0))

        life_lost_text = self.font.render(f"¡Perdiste una vida! Te quedan {self.lives}", True, WHITE)
        continue_text = self.font.render("Continuar...", True, WHITE)

        self.screen.blit(life_lost_text, (SCREEN_WIDTH // 2 - life_lost_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - 25))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 25))

        pygame.display.flip()
        pygame.time.wait(2000)  # Esperar 2 segundos


if __name__ == "__main__":
    game = MathBreakout()
    game.run()
    pygame.quit()
