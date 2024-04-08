import time

import pygame, sys
import random
from Colors import *

# global variables
screen_width, screen_height = 800,600
bg_color = BLACK
clock = pygame.time.Clock()

#initializing the pygame
pygame.init()

#set up the screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snack Game")



speed=10
bodySize = speed
score= 0
direction = "Up"
change_to=direction


# snake
head_Pos=[100,100]
body_positions=[[100,100],
                [100+speed, 100],
                [100+2*speed, 100]]

#food
food_position =[random.randint(1,((screen_width-bodySize)//speed)) * speed,
                random.randint(1,((screen_height-bodySize)//speed)) * speed]
spawn_Food=True

# fonctions
def UpdateScore_text(font, size):
    score_font = pygame.font.SysFont(font, size)
    text_surface = score_font.render("Score : " + str(score), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (60, 10)
    screen.blit(text_surface, text_rect)

def GameOver():
    for body in body_positions[1:]:
        if  body[0]==head_Pos[0] and body[1] == head_Pos[1]:
            return True
    return False

def Update_GameOverFont(font,size):
    gameover_font = pygame.font.SysFont(font, size)
    game_over_text = gameover_font.render("Game Over", True, (255, 0, 0))  # Render game over text
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))  # Center the text
    screen.blit(game_over_text, game_over_rect)  # Draw game over text
    pygame.display.update()  # Update the display

def restart():
    global speed, body_size, score, direction, change_to, head_pos, body_positions, food_position, spawn_food

    speed = 10
    bodySize = speed
    score = 0
    direction = "Up"
    change_to = direction

    head_Pos = [100, 100]
    body_positions = [[100, 100],
                      [100 + speed, 100],
                      [100 + 2 * speed, 100]]

    # food
    food_position = [random.randint(1, ((screen_width - bodySize) // speed)) * speed,
                     random.randint(1, ((screen_height - bodySize) // speed)) * speed]
    spawn_Food = True

def Draw():
    global  bodySize, body_positions,food_position
    for i in range(len(body_positions)):
        color=RED
        if i == 0:
           color=BLUE
        pygame.draw.rect(screen, color, pygame.Rect(body_positions[i][0], body_positions[i][1], bodySize, bodySize))

    pygame.draw.rect(screen, YELLOW, pygame.Rect(food_position[0], food_position[1], bodySize, bodySize))

def SnakeGrowth():
    global body_positions,bodySize, head_Pos,food_position,speed, spawn_Food,score
    body_positions.insert(0, list(head_Pos))
    if head_Pos[0] == food_position[0] and head_Pos[1] == food_position[1]:
        score += 10
        spawn_Food = False
    else:
        body_positions.pop()

    if not spawn_Food:
        food_position = [random.randint(1, ((screen_width - bodySize) // speed)) * speed,
                         random.randint(1, ((screen_height - bodySize) // speed)) * speed]

    spawn_Food = True

def HandleSnakeMove():
    global change_to,direction,head_Pos
    if change_to == "Up" and direction != "Down":
        direction = "Up"
    if change_to == "Down" and direction != "Up":
        direction = "Down"
    if change_to == "Left" and direction != "Right":
        direction = "Left"
    if change_to == "Right" and direction != "Left":
        direction = "Right"

    if direction == "Up":
        head_Pos[1] -= speed
    if direction == "Down":
        head_Pos[1] += speed
    if direction == "Right":
        head_Pos[0] += speed
    if direction == "Left":
        head_Pos[0] -= speed

    if head_Pos[0] < 0:
        head_Pos[0] = screen_width
    if head_Pos[0] > screen_width:
        head_Pos[0] = 0
    if head_Pos[1] < 0:
        head_Pos[1] = screen_height
    if head_Pos[1] > screen_height:
        head_Pos[1] = 0

# the game main loop
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Moving the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                change_to="Down"

            if event.key == pygame.K_UP :
                change_to="Up"

            if event.key == pygame.K_LEFT :
                change_to="Left"


            if event.key == pygame.K_RIGHT:
                change_to="Right"


    HandleSnakeMove()

    if GameOver():
        Update_GameOverFont('times new roman',50)
        time.sleep(2)
        restart()

    #Visuals
    screen.fill(bg_color)
    SnakeGrowth()
    Draw()

    UpdateScore_text('times new roman',20)

    #updating the screen
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()