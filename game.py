import pygame
import os
import time
import random

pygame.font.init()
pygame.init()
pygame.display.set_caption("Arkanoid")
#Game constants:
WIDTH,HEIGHT = 800, 600
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 80, 20
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
BALL_WIDTH, BALL_HEIGHT = 20,20
PLAYER_VEL = 10
GAME_OBJ = []
score = 0
main_font = pygame.font.SysFont("Comicsans", 20)
#Game images
BG = pygame.transform.scale(pygame.image.load(os.path.join("data", "background.jpg")), (WIDTH,HEIGHT))
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join("data", "player.png")),(PLAYER_WIDTH,PLAYER_HEIGHT))
BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "purple_brick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
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
        self.mask = pygame.mask.from_surface(self.player_img)
    def draw(self, window):
        window.blit(self.player_img,(self.x, self.y))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ball_img = BALL
        self.mask = pygame.mask.from_surface(self.ball_img)
        self.ball_vel_x = 4
        self.ball_vel_y = 5
        self.points = 0

    def draw(self, window):
        window.blit(self.ball_img, (self.x, self.y))

    def update_position(self):

        self.x += self.ball_vel_x
        self.y += self.ball_vel_y

        if self.x < 0 or self.x > WIDTH - BALL_WIDTH:
            self.ball_vel_x = -self.ball_vel_x
        if self.y < 0 or self.y > HEIGHT - BALL_HEIGHT:
            self.ball_vel_y = -self.ball_vel_y

        for obj in GAME_OBJ:
            if collide(self, obj):
                if isinstance(obj, Brick):
                    GAME_OBJ.remove(obj)
                    self.points += 10
                    self.ball_vel_y = -self.ball_vel_y
                elif isinstance(obj, Player):
                    self.ball_vel_y = -self.ball_vel_y
                    self.ball_vel_x = (self.x - obj.x) / (PLAYER_WIDTH / 2)



class Brick:
    def __init__(self, x, y, lives = 1):
        self.x = x
        self.y = y
        self.lives = lives
        self.brick_img = BRICK
        self.mask = pygame.mask.from_surface(self.brick_img)
    
    def draw(self, window):
        window.blit(self.brick_img, (self.x, self.y))

class BrickPanel:
    def __init__(self, brick_width=60, brick_height=20, brick_rows=5, brick_columns=12):
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_rows = brick_rows
        self.brick_columns = brick_columns
        self.bricks = self.create_bricks()

    def create_bricks(self):
        bricks = []
        x_gap = 40
        y_gap = 30
        for row in range(self.brick_rows):
            for col in range(self.brick_columns):
                x = col * self.brick_width + x_gap
                y = row * self.brick_height + y_gap
                brick = Brick(x, y)
                bricks.append(brick)
        return bricks
    
    def draw(self, window):
        for brick in self.bricks:
            brick.draw(window)
        
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    running = True
    player = Player(300,550)
    brick_panel = BrickPanel()
    ball = Ball(400, 300)
    bricks = brick_panel.bricks

    GAME_OBJ.extend(bricks)
    GAME_OBJ.append(player)
    GAME_OBJ.append(ball)

    

    def redraw_window():
        screen.blit(BG, (0,0))
        
        points_label = main_font.render(f"Points: {ball.points}", 1, (255,255,255))
        screen.blit(points_label, (0,5))
        
        for obj in GAME_OBJ:
            obj.draw(screen)

        ball.update_position()
        pygame.display.update()
        

    while running:
        clock.tick(FPS)
        if len(GAME_OBJ) == 2:
            running = False
        redraw_window()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x < WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_VEL
        if ball.y == HEIGHT - BALL_HEIGHT:
            break
        

main()