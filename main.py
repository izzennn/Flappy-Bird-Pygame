import pygame
import math
import sys
import random

pygame.init()
pygame.mixer.init()

# Screen dimensions
screen_x = 625
screen_y = 800
tile_width = 25
tile_height = 80

# Create the screen
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (87, 136, 73)
DARKGREEN = (0, 100, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128, 255)

# Game states
running = True
game_start = False
alive = True
game_over_state = False
current_score = 0  # Initialize the score

# Fonts
font = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 100)
font2 = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 115)
font3 = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 50)

# Sounds
pygame.mixer.music.load("background.wav")
jump_sound = pygame.mixer.Sound("jump.wav")
col_sound = pygame.mixer.Sound("col.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Images
bird_image = pygame.image.load("bird.png")  # Regular bird image
bird_jump_image = pygame.image.load("birdjump.png")  # Jumping bird image
pipe_image = pygame.image.load("pipes.png")
background = pygame.image.load('flappy_bird_background.png')
button_img = pygame.image.load('CGB01-green_L_rounded_btn.png')

class movingBird:
    def __init__(self, x_tile, y_tile, bird_image):
        self.resized_image = pygame.transform.scale(bird_image, (200,200))
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x = self.x_tile * tile_width
        self.y = self.y_tile * tile_height
        self.rect = self.resized_image.get_rect()

    def display(self):
        screen.blit(self.resized_image, self.rect)
        self.rect.topleft = (self.x, self.y)

    def move(self):
        self.x_tile += 0.2
        self.x = self.x_tile * tile_width
        if self.x_tile > 25:
            self.x_tile = -5

# Bird class
class Bird:
    def __init__(self, x_tile, y_tile, color, bird_image, bird_jump_image):
        self.resized_image = pygame.transform.scale(bird_image, (100, 100))
        self.resized_jump_image = pygame.transform.scale(bird_jump_image, (70, 70))
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x = self.x_tile * tile_width
        self.y = self.y_tile * tile_height
        self.color = color
        self.jump = False
        self.rect = self.resized_image.get_rect()
        self.alive = True

    def display(self):
        # Display the bird image based on jump state
        if self.jump:
            screen.blit(self.resized_jump_image, self.rect)
        else:
            screen.blit(self.resized_image, self.rect)
        self.rect.topleft = (self.x - 25, self.y - 25)

    def move(self):
        # Move the bird upwards when jumping
        if self.jump and self.alive:
            self.y_tile -= 0.1
            self.y = self.y_tile * tile_height
            self.rect.topleft = (self.x - 25, self.y - 25)
            jump_sound.play()

    def gravity(self, force):
        # Apply gravity to the bird
        if not self.jump:
            self.y_tile += force
            self.y = self.y_tile * tile_height
        self.rect.topleft = (self.x - 25, self.y - 25)

# Pipe class
class Pipes:
    def __init__(self, x_tile, y_tile, color, down, pipe_img):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x = self.x_tile * tile_width
        self.y = self.y_tile * tile_height
        self.color = color
        self.downpipe = down
        self.rect = pygame.Rect(self.x, self.y, 4 * tile_width, 10 * tile_height)

    def display(self):
        # Draw the pipe
        pygame.draw.rect(screen, self.color, (self.x, self.y, 4 * tile_width, 10 * tile_height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 4 * tile_width, 10 * tile_height), 3)
        self.rect.topleft = (self.x, self.y)

    def move(self):
        # Move the pipe leftward
        self.x_tile -= 0.5
        self.x = self.x_tile * tile_width
        if self.x_tile < -1:
            self.x_tile = 27
            if self.downpipe:
                self.y_tile = random.uniform(5, 9)
            else:
                self.y_tile = random.uniform(-9, -5)

            self.y = self.y_tile * tile_height
        self.rect.topleft = (self.x, self.y)

# Button class
class Button:
    def __init__(self, x_tile, y_tile, img):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x = self.x_tile * tile_width
        self.y = self.y_tile * tile_height
        self.res_x = 400
        self.res_y = 100
        self.img = img
        self.resized_img = pygame.transform.scale(self.img, (self.res_x, self.res_y))
        self.rect = self.resized_img.get_rect()

    def display(self):
        # Display the button
        screen.blit(self.resized_img, self.rect)
        self.rect.topleft = (self.x, self.y)

    def zoom(self):
        # Zoom the button on hover
        if self.res_x < 420 and self.res_y < 120:
            self.resized_img = pygame.transform.scale(self.img, (self.res_x + 20, self.res_y + 20))
            self.x -= 0.1
            self.y -= 0.2
        self.rect.topleft = (self.x, self.y)

    def unZoom(self):
        # Reset button size
        self.resized_img = pygame.transform.scale(self.img, (self.res_x, self.res_y))
        self.x = self.x_tile * tile_width
        self.y = self.y_tile * tile_height
        self.rect.topleft = (self.x, self.y)

# Instantiate bird, button, and pipes
bird = Bird(12, 5, BLACK, bird_image, bird_jump_image)
movingbird = movingBird(8, 3, bird_image)
button = Button(4.2, 6, button_img)

pipes = [
    Pipes(27, -7, GREEN, False, pipe_image),  # Upper pipe
    Pipes(27, 8, GREEN, True, pipe_image),    # Lower pipe
    Pipes(40, -6, GREEN, False, pipe_image),  # Upper pipe
    Pipes(40, 9, GREEN, True, pipe_image)     # Lower pipe
]

# Collision detection
def collisions():
    global alive
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect):
            jump_sound.stop()
            score_sound.stop()
            col_sound.play()
            bird.alive = False
            bird.gravity(0.5)
            alive = False

# Opening screen
def openingScreen():
    screen.blit(background, (0,0))
    button.display()
    movingbird.move()
    movingbird.display()
    if (mouse_x >= button.x and mouse_x <= button.x + 400) and (mouse_y >= button.y and mouse_y <= button.y + 100):
        button.zoom()
        button.display()
    else:
        button.unZoom()
    opening_text = font2.render("Flappy Bird", True, BLACK)
    screen.blit(opening_text, (5, 130))
    start_text = font2.render("START", True, BLACK)
    screen.blit(start_text, (5.4 * tile_width, 5.7 * tile_height))

# Score update and display
def score():
    global current_score
    for pipe in pipes:
        if bird.x >= pipe.x and bird.x <= pipe.x + 4 * tile_width:
            if bird.x == pipe.x + 2 * tile_width:
                jump_sound.stop()
                score_sound.play()
                current_score += 1
                break

def display_score():
    score_text = font.render(str(current_score), True, BLACK)
    screen.blit(score_text, (10, 10))  # Display the score at the top-left corner

# Game over display
def game_over():
    global game_over_state
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (80, 300))
    restart_text = font3.render("SpaceBar to Restart", True, BLACK)
    screen.blit(restart_text, (60, 400))
    game_over_state = True

# Reset the game state
def reset_game():
    global bird, pipes, current_score, alive, game_over_state
    bird = Bird(12, 5, BLACK, bird_image, bird_jump_image)
    pipes = [
        Pipes(27, -7, GREEN, False, pipe_image),
        Pipes(27, 8, GREEN, True, pipe_image),
        Pipes(40, -6, GREEN, False, pipe_image),
        Pipes(40, 9, GREEN, True, pipe_image)
    ]
    current_score = 0
    alive = True
    game_over_state = False

# Main game loop
pygame.mixer.music.play(loops=-1)
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_start:
                bird.jump = True
            if event.key == pygame.K_SPACE and game_over_state:
                reset_game()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and game_start:
                bird.jump = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (mouse_x >= button.x and mouse_x <= button.x + 400) and (mouse_y >= button.y and mouse_y <= button.y + 100):  # Left click
                pygame.mixer.music.stop()
                col_sound.play()
                game_start = True
    if game_start:
        pygame.mixer.music.stop()
        screen.blit(background, (0, 0))
        if bird.alive:
            collisions()
            score()  # Update the score
        bird.gravity(0.03)
        bird.move()
        bird.display()
        for pipe in pipes:
            if alive:
                pipe.move()
            pipe.display()
        display_score()  # Display the score
        if not bird.alive:
            game_over()
    else:
        openingScreen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
