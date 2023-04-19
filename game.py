import pygame
import os
import time
import random

pygame.init()
pygame.display.set_caption("Arkanoid")

#Game constants:
WIDTH,HEIGHT = 800, 600
FPS = 60
BG = pygame.transform.scale(pygame.image.load(os.path.join("data", "background.jpg")), (WIDTH,HEIGHT))


screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, lives = 1):
        self.x = x
        self.y = y
        self.lives = lives
        self.player_img = None

    def draw(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))

def main():
    running = True
    player = Player(300,450)

    def redraw_window():
        screen.blit(BG, (0,0))
        player.draw(screen)
        pygame.display.update()
        

    while running:
        clock.tick(FPS)
        redraw_window()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        

main()