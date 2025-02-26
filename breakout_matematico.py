import pygame
import random
import os
import numpy as np

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

class MathBreakout:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Math Breakout Adventure")
        self.clock = pygame.time.Clock()
        
        # Load sounds
        self.load_sounds()
        
        # Load fonts
        self.title_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 36)
        
        # Load background
        self.background = self.create_background()
        
        self.reset_game(1)

    def load_sounds(self):
        try:
            self.brick_hit_sound = pygame.mixer.Sound(os.path.join('sounds', 'brick_hit.wav'))
            self.wrong_answer_sound = pygame.mixer.Sound(os.path.join('sounds', 'wrong_answer.wav'))
            self.game_over_sound = pygame.mixer.Sound(os.path.join('sounds', 'game_over.wav'))
        except Exception as e:
            print(f"Error loading sounds: {e}")
            # Fallback to basic sound generation
            sample_rate = 44100
            duration = 1  # 1 second
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = 0.5 * np.sin(2 * np.pi * 440 * t)  # Generate a 440 Hz sine wave
            wave = np.tile(wave, (2, 1)).T  # Make it 2-dimensional for stereo
            self.brick_hit_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(wave))
            self.wrong_answer_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(wave * 0.5))
            self.game_over_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(wave * 0.25))

    def create_background(self):
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(BLACK)
        
        # Add some starry effect
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(background, WHITE, (x, y), random.randint(1, 3))
        
        return background

    def reset_game(self, level):
        self.level = level
        self.score = 0
        self.lives = 6
        self.paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, 
                                   SCREEN_HEIGHT - 50, 
                                   PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, 
                                 SCREEN_HEIGHT // 2 - BALL_RADIUS, 
                                 BALL_RADIUS * 2, BALL_RADIUS * 2)
        # Increase ball speed and difficulty with each level
        self.ball_speed_x = 5 + (self.level * 0.5)
        self.ball_speed_y = -(5 + (self.level * 0.5))
        self.create_bricks()

    def create_bricks(self):
        self.bricks = []
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        for row in range(5 + self.level):
            for col in range(10):
                brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 50, 
                                    row * (BRICK_HEIGHT + 5) + 50, 
                                    BRICK_WIDTH, BRICK_HEIGHT)
                # Assign different colors based on row and level
                brick_color = colors[row % len(colors)]
                self.bricks.append((brick, brick_color))

    def generate_math_problem(self):
        # Increase problem complexity with level
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
        else:  # Division for higher levels
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            problem = f"{a} ÷ {b} = ?"
            answer = a // b

        return problem, answer

    def show_math_problem(self, problem):
        original_screen = self.screen
        problem_screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Math Challenge")
        
        input_box = pygame.Rect(150, 200, 100, 50)
        color_inactive = BLUE
        color_active = GREEN
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            try:
                                user_answer = int(text)
                                self.screen = original_screen
                                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                                return user_answer
                            except ValueError:
                                text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            problem_screen.fill(WHITE)
            problem_txt = self.font.render(problem, True, BLACK)
            problem_screen.blit(problem_txt, (100, 100))
            
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            problem_screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(problem_screen, color, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def show_game_over(self):
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera 3 segundos

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
                self.ball.top = self.paddle.top - self.ball.height
                self.ball_speed_y *= -1

            # Colisión con los ladrillos
            for brick_data in self.bricks[:]:
                brick, color = brick_data
                if self.ball.colliderect(brick):
                    # Ajustar la posición de la bola según el lado de colisión
                    if abs(self.ball.bottom - brick.top) < 10 and self.ball_speed_y > 0:
                        self.ball.bottom = brick.top
                    elif abs(self.ball.top - brick.bottom) < 10 and self.ball_speed_y < 0:
                        self.ball.top = brick.bottom
                    elif abs(self.ball.right - brick.left) < 10 and self.ball_speed_x > 0:
                        self.ball.right = brick.left
                    elif abs(self.ball.left - brick.right) < 10 and self.ball_speed_x < 0:
                        self.ball.left = brick.right

                    self.ball_speed_y *= -1 if abs(self.ball.bottom - brick.top) < 10 or abs(self.ball.top - brick.bottom) < 10 else self.ball_speed_y
                    self.ball_speed_x *= -1 if abs(self.ball.right - brick.left) < 10 or abs(self.ball.left - brick.right) < 10 else self.ball_speed_x

                    problem, correct_answer = self.generate_math_problem()
                    user_answer = self.show_math_problem(problem)

                    if user_answer == correct_answer:
                        self.brick_hit_sound.play()
                        self.score += 100
                        self.bricks.remove(brick_data)
                    else:
                        self.wrong_answer_sound.play()
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over_sound.play()
                            self.show_game_over()
                            running = False
                        else:
                            # Mover la bola de nuevo a la posición inicial
                            self.ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                            self.ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS

                    # Mantener una velocidad constante
                    self.ball_speed_x = 5
                    self.ball_speed_y = -5

            # Dibujo
            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, BLUE, self.paddle)
            pygame.draw.ellipse(self.screen, WHITE, self.ball)

            # Dibujar ladrillos con colores
            for brick, color in self.bricks:
                pygame.draw.rect(self.screen, color, brick)

            # Mostrar puntuación y vidas
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)

            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(level_text, (10, 90))

            # Condiciones de game over
            if self.ball.bottom >= SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over_sound.play()
                    self.show_game_over()
                    running = False
                else:
                    # Mover la bola de nuevo a la posición inicial
                    self.ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                    self.ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS
                    #self.ball_speed_x *= 0.4
                    #self.ball_speed_y *= 0.4

            # Nivel completado
            if not self.bricks:
                self.level += 1
                self.reset_game(self.level)

            pygame.display.flip()
            self.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game = MathBreakout()
    game.run()
