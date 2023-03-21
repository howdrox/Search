import pygame
import random
import heapq

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the dimensions of the board
BOARD_WIDTH = 20
BOARD_HEIGHT = 15

# Set the dimensions of the blocks
BLOCK_WIDTH = SCREEN_WIDTH // BOARD_WIDTH
BLOCK_HEIGHT = SCREEN_HEIGHT // BOARD_HEIGHT

# Define the directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Define the game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Search: A game of shortest path")
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.player = Person(self.board, BLUE)
        self.bot = Person(self.board, RED)
        self.bot.strategy = "astar"  # Change this to "random" for a random strategy
        self.score = 0
        self.high_score = 0
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill(WHITE)
            
            # Move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player.move(UP)
            elif keys[pygame.K_DOWN]:
                self.player.move(DOWN)
            elif keys[pygame.K_LEFT]:
                self.player.move(LEFT)
            elif keys[pygame.K_RIGHT]:
                self.player.move(RIGHT)
            
            # Move the bot
            if self.bot.strategy == "random":
                self.bot.move_random()
            else:
                self.bot.move_astar(self.player)
            
            # Draw the board, player and bot
            self.board.draw(self.screen)
            self.player.draw(self.screen)
            self.bot.draw(self.screen)
            
            # Check if the player and bot collide
            if self.player.rect.colliderect(self.bot.rect):
                self.game_over()
            
            # Update the score
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            
            # Update the screen
            pygame.display.flip()
            self.clock.tick(10 + self.score // 50)  # Increase the speed of the bot
            
        pygame.quit()
    
    def game_over(self):
        self.running = False
        print(f"Game over! Score: {self.score}, High Score: {self.high_score}")

# Define the person class
class Person(pygame.sprite.Sprite):
    def __init__(self, board, color):
        super().__init__()
        self.board = board
        self.color = color
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(BOARD_WIDTH) * BLOCK_WIDTH
        self.rect.y = random.randrange(BOARD_HEIGHT) * BLOCK_HEIGHT
    
    def move(self, direction):
        new_rect = self.rect.move([direction[1] * BLOCK_WIDTH, direction[0] * BLOCK_HEIGHT
