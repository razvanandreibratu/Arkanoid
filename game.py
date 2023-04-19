import pygame
import os
import time
import random

pygame.init()
pygame.display.set_caption("Arkanoid")

#Game constants:
WIDTH,HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 80, 20
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
BALL_WIDTH, BALL_HEIGHT = 20,20
#Game images
BG = pygame.transform.scale(pygame.image.load(os.path.join("data", "background.jpg")), (WIDTH,HEIGHT))
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join("data", "player.png")),(PLAYER_WIDTH,PLAYER_HEIGHT))
BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "brick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
BALL = pygame.transform.scale(pygame.image.load(os.path.join("data", "ball.png")), (BALL_WIDTH, BALL_HEIGHT))
#Game BG and TICK rate
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, lives = 1):
        self.x = x
        self.y = y
        self.lives = lives
        self.player_img = PLAYER
    def draw(self, window):
        window.blit(self.player_img,(self.x, self.y))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ball_img = BALL
    def draw(self, window):
        window.blit(self.ball_img, (self.x, self.y))

class Brick:
    def __init__(self, x, y, lives = 1):
        self.x = x
        self.y = y
        self.lives = lives
        self.brick_img = BRICK
    
    def draw(self, window):
        window.blit(self.brick_img, (self.x, self.y))

class BrickPanel:
    def __init__(self, window_width = WIDTH, window_height = HEIGHT, brick_width=60, brick_height=20, brick_spacing=10, brick_rows=5, brick_columns=10):
        self.window_width = window_width
        self.window_height = window_height
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_spacing = brick_spacing
        self.brick_rows = brick_rows
        self.brick_columns = brick_columns
        self.bricks = self.create_bricks()
    
    def create_bricks(self):
        bricks = []
        for row in range(self.brick_rows):
            for col in range(self.brick_columns):
                x = col * (self.brick_width + self.brick_spacing) + self.brick_spacing
                y = row * (self.brick_height + self.brick_spacing) + self.brick_spacing
                brick = Brick(x, y)
                bricks.append(brick)
        return bricks
    
    def draw(self, window):
        for brick in self.bricks:
            brick.draw(window)

def main():
    running = True
    player = Player(300,550)
    brick_panel = BrickPanel()
    ball = Ball(330, 530)

    def redraw_window():
        screen.blit(BG, (0,0))
        player.draw(screen)
        brick_panel.draw(screen)
        ball.draw(screen)

        pygame.display.update()
        

    while running:
        clock.tick(FPS)
        redraw_window()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        

main()