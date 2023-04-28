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
#Color constants
WHITE = (255,255,255)
#Game font
main_font = pygame.font.SysFont("Comicsans", 20)
#Game images
BG = pygame.transform.scale(pygame.image.load(os.path.join("data", "background.jpg")), (WIDTH,HEIGHT))
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join("data", "player.png")),(PLAYER_WIDTH,PLAYER_HEIGHT))
#Bricks in game
PURPLE_BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "purplebrick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
GREEN_BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "greenbrick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
ORANGE_BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "orangebrick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
RED_BRICK = pygame.transform.scale(pygame.image.load(os.path.join("data", "redbrick.png")),(BRICK_WIDTH, BRICK_HEIGHT))
#Ball
BALL = pygame.transform.scale(pygame.image.load(os.path.join("data", "ball.png")), (BALL_WIDTH, BALL_HEIGHT))
#Game BG and TICK rate
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#Game classes 
class Player:
    def __init__(self, x, y, lives = 2):
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
        self.started = False

    def draw(self, window):
        window.blit(self.ball_img, (self.x, self.y))

    def update_position(self):
        if not self.started:
            return
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
                    self.points += obj.hit()
                    self.ball_vel_y = -self.ball_vel_y
                elif isinstance(obj, Player):
                    self.ball_vel_y = -self.ball_vel_y
                    self.ball_vel_x = (self.x - obj.x) / (PLAYER_WIDTH / 2)
    def get_points(self):
        return self.points

class Brick:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points
        self.brick_img = None
        self.mask = None
    def draw(self, window):
        window.blit(self.brick_img, (self.x, self.y))
    def hit(self):
        return self.points
    
class PurpleBrick(Brick):
    def __init__(self, x, y, points):
        super().__init__(x, y, points)
        self.brick_img = PURPLE_BRICK
        self.mask = pygame.mask.from_surface(self.brick_img)

class RedBrick(Brick):
    def __init__(self, x, y, points):
        super().__init__(x, y, points)
        self.brick_img = RED_BRICK
        self.mask = pygame.mask.from_surface(self.brick_img)

class OrangeBrick(Brick):
    def __init__(self, x, y, points):
        super().__init__(x, y, points)
        self.brick_img = ORANGE_BRICK
        self.mask = pygame.mask.from_surface(self.brick_img)

class GreenBrick(Brick):
    def __init__(self, x, y, points):
        super().__init__(x, y, points)
        self.brick_img = GREEN_BRICK
        self.mask = pygame.mask.from_surface(self.brick_img)

#Game methods  
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
#Generate first level
def create_bricks():
    bricks = []
    brick_rows = 5
    brick_columns = 12
    x_gap = 40
    y_gap = 30
    for row in range(brick_rows):
        for col in range(brick_columns):
            x = col * BRICK_WIDTH + x_gap
            y = row * BRICK_HEIGHT + y_gap
            color = random.choice(['green', 'purple', 'red', 'orange'])
            points = random.randint(10, 100)
            if color == 'green':
                brick = GreenBrick(x, y, points)
            elif color == 'purple':
                brick = PurpleBrick(x, y, points)
            elif color == 'red':
                brick = RedBrick(x, y, points)
            elif color == 'orange':
                brick = OrangeBrick(x, y, points)
            bricks.append(brick)
    return bricks
#Game menus
#TODO main menu
def main_menu():
    return
#TODO pause menu 
def pause_menu(points):
    game_pause = True
    pause_font = pygame.font.SysFont("Comicsans", 50)

    def draw():
       screen.blit(BG,(0,0))
       pause_label_points = pause_font.render(f"POINTS: {points}", 1, WHITE)
       screen.blit(pause_label_points, (250,100))   

       pause_label_continue = pause_font.render("Press space to continue...", 1, WHITE)
       screen.blit(pause_label_continue, (100, 220))

       pause_label_exit = pause_font.render("Exit", 1, WHITE)
       screen.blit(pause_label_exit, (330,400))
       pygame.display.update()

    while game_pause:
        draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_pause = False
                return game_pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False
                    return not game_pause

#TODO losing screen and points
def losing_menu(points, name):
    #TODO implement a loser background
    loser = True
    loser_font = pygame.font.SysFont("Comicsans", 50)
    def draw():
        screen.blit(BG, (0, 0))

        losing_label_points = loser_font.render(f"Points: {points}", 1, WHITE)
        screen.blit(losing_label_points, (250, 100))
        losing_label_name = loser_font.render(f"You lost: {name}", 1, WHITE)
        screen.blit(losing_label_name, (100, 220))

        pygame.display.update()

    while loser:
        draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loser = False
                return loser
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    loser = False
                    return not loser
                    

#TODO handling winning action
def winner():
    pass

#Game main functions
def main():
    running = True
    player = Player(300, 550)
    ball = Ball(330, 530)
    bricks = create_bricks()

    GAME_OBJ.extend(bricks)
    GAME_OBJ.append(player)
    GAME_OBJ.append(ball)

    def redraw_window():
        screen.blit(BG, (0,0))

        points_label = main_font.render(f"Points: {ball.points}", 1, WHITE)
        screen.blit(points_label, (5,0))
        lives_label = main_font.render(f"Lives: {player.lives}", 1, WHITE)
        screen.blit(lives_label, (720, 0))

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
            if not ball.started:
                ball.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x < WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_VEL
            if not ball.started:
                ball.x += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            ball.started = True
        if keys[pygame.K_p]:
            running = pause_menu(ball.get_points())

        #LOSING GAME LOGIC
        if ball.y == HEIGHT - BALL_HEIGHT:
            player.lives -= 1
            if player.lives == 0:
                running = losing_menu(ball.get_points(), "Dorel")
                running = False
            ball.started = False
            ball.y = player.y - 20
            ball.x = player.x + 30
        

main()

#TODO implement highscore
#TODO implement music
#TODO implement power ups
#TODO implement level
#TODO implement unbreakable bricks
