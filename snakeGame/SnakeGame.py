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


class Snake:
    def __init__(self,speed,size,score,direction, head_Pos):
        self.speed = speed
        self.bodySize = size
        self.score = score
        self.direction = direction
        self.change_to = self.direction
        self.head_Pos = head_Pos
        self.body_positions = [list(head_Pos),
                               [list(head_Pos)[0]+self.speed,list(head_Pos)[1]],
                               [list(head_Pos)[0]+2*self.speed,list(head_Pos)[1]]]
        self.food_position = [random.randint(1, ((screen_width - self.bodySize) // self.speed)) * self.speed,
                              random.randint(1, ((screen_height - self.bodySize) // self.speed)) * self.speed]
        self.spawn_food = True

    def HandleSnakeMove(self):
        if self.change_to == "Up" and self.direction != "Down":
            self.direction = "Up"
        if self.change_to == "Down" and self.direction  != "Up":
            self.direction  = "Down"
        if self.change_to == "Left" and self.direction  != "Right":
            self.direction = "Left"
        if self.change_to == "Right" and self.direction  != "Left":
            self.direction  = "Right"

        if self.direction  == "Up":
            self.head_Pos[1] -= self.speed
        if self.direction  == "Down":
            self.head_Pos[1] += self.speed
        if self.direction  == "Right":
            self.head_Pos[0] += self.speed
        if self.direction  == "Left":
            self.head_Pos[0] -= self.speed

        if self.head_Pos[0] < 0:
            self.head_Pos[0] = screen_width
        if self.head_Pos[0] > screen_width:
            self.head_Pos[0] = 0
        if self.head_Pos[1] < 0:
            self.head_Pos[1] = screen_height
        if self.head_Pos[1] > screen_height:
            self.head_Pos[1] = 0

    def SnakeGrowth(self):
        self.body_positions.insert(0, list(self.head_Pos))
        if self.head_Pos[0] == self.food_position[0] and self.head_Pos[1] == self.food_position[1]:
            self.score += 10
            self.spawn_food = False
        else:
            self.body_positions.pop()

        if not self.spawn_food:
            self.food_position = [random.randint(1, ((screen_width - self.bodySize) // self.speed)) * self.speed,
                             random.randint(1, ((screen_height - self.bodySize) // self.speed)) * self.speed]

        self.spawn_food = True

    def Draw(self,):
        for i in range(len(self.body_positions)):
            color = RED
            if i == 0:
                color = BLUE
            pygame.draw.rect(screen, color, pygame.Rect(self.body_positions[i][0], self.body_positions[i][1], self.bodySize, self.bodySize))

        pygame.draw.rect(screen, YELLOW, pygame.Rect(self.food_position[0], self.food_position[1], self.bodySize, self.bodySize))

    def restart(self,speed,size,score,direction, head_Pos):
        self.speed = speed
        self.bodySize = self.speed
        self.score = score
        self.direction = direction
        self.change_to = self.direction
        self.head_Pos = head_Pos
        self.body_positions = [list(head_Pos),
                               [list(head_Pos)[0] + self.speed, list(head_Pos)[1]],
                               [list(head_Pos)[0] + 2 * self.speed, list(head_Pos)[1]]]
        # food
        self.food_position = [random.randint(1, ((screen_width - self.bodySize) // self.speed)) * self.speed,
                         random.randint(1, ((screen_height - self.bodySize) // self.speed)) * self.speed]
        self.spawn_food = True

    def GameOver(self):
        for body in self.body_positions[1:]:
            if body[0] == self.head_Pos[0] and body[1] == self.head_Pos[1]:
                return True
        return False


#creating new snake
snake = Snake(10,10,0,"Up",[100,100])

# fonctions
def UpdateScore_text(font, size):
    score_font = pygame.font.SysFont(font, size)
    text_surface = score_font.render("Score : " + str(snake.score), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (60, 10)
    screen.blit(text_surface, text_rect)

def Update_GameOverFont(font,size):
    gameover_font = pygame.font.SysFont(font, size)
    game_over_text = gameover_font.render("Game Over", True, (255, 0, 0))  # Render game over text
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))  # Center the text
    screen.blit(game_over_text, game_over_rect)  # Draw game over text
    pygame.display.update()  # Update the display


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
                snake.change_to="Down"

            if event.key == pygame.K_UP :
                snake.change_to="Up"

            if event.key == pygame.K_LEFT :
                snake.change_to="Left"


            if event.key == pygame.K_RIGHT:
                snake.change_to="Right"


    snake.HandleSnakeMove()

    if snake.GameOver():
        Update_GameOverFont('times new roman', 50)
        time.sleep(2)
        snake.restart(10, 10, 0, "Up", [100, 100])

    #Visuals
    screen.fill(bg_color)
    snake.SnakeGrowth()
    snake.Draw()


    UpdateScore_text('times new roman',20)

    #updating the screen
    pygame.display.flip()
    clock.tick(snake.speed)

pygame.quit()