import time

import pygame, sys
import random
from Colors import *
import  numpy as np

#initializing the pygame
pygame.init()


class SnakeGameAI:
    def __init__(self):
        # init screen
        self.screen_width, self.screen_height = 800, 600
        self.bg_color = BLACK
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snack Game")
        self.running = True
        self.reward = 0


        # init snake
        self.restart()

    def HandleSnakeMove(self, action):
        #[staight, right, left]

        clock_wise = ["Up","Right","Down","Left"]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):#staight no change
            self.direction = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]): #right
            next_idx = (idx + 1) % 4
            self.direction = clock_wise[next_idx]
        else: #left [0,0,1]
            next_idx = (idx - 1) % 4
            self.direction = clock_wise[next_idx]

        if self.direction  == "Up":
            self.head_Pos[1] -= self.speed
        if self.direction  == "Down":
            self.head_Pos[1] += self.speed
        if self.direction  == "Right":
            self.head_Pos[0] += self.speed
        if self.direction  == "Left":
            self.head_Pos[0] -= self.speed



    def SnakeGrowth(self, reward):
        self.body_positions.insert(0, list(self.head_Pos))
        if self.head_Pos == self.food_position:
            self.score += 1
            self.reward = 10
            self.spawn_food = False
        else:
            self.body_positions.pop()

        if not self.spawn_food:
            self.food_position = [random.randint(1, ((self.screen_width - self.bodySize) // self.speed)) * self.speed,
                             random.randint(1, ((self.screen_height - self.bodySize) // self.speed)) * self.speed]

        self.spawn_food = True

    def Draw(self,):
        for i in range(len(self.body_positions)):
            color = RED
            if i == 0:
                color = BLUE
            pygame.draw.rect(self.screen, color, pygame.Rect(self.body_positions[i][0], self.body_positions[i][1], self.bodySize, self.bodySize))

        pygame.draw.rect(self.screen, YELLOW, pygame.Rect(self.food_position[0], self.food_position[1], self.bodySize, self.bodySize))

    def restart(self):
        self.speed = 10
        self.bodySize = self.speed
        self.score = 0
        self.direction = "Up"
        self.head_Pos = [100, 100]
        self.body_positions = [[100, 100],
                               [100 + self.speed, 100],
                               [100 + 2 * self.speed, 100]]
        # food
        self.food_position = [random.randint(1, ((self.screen_width - self.bodySize) // self.speed)) * self.speed,
                         random.randint(1, ((self.screen_height - self.bodySize) // self.speed)) * self.speed]
        self.spawn_food = True
        self.frame_iteration = 0


    def GameOver(self, pt=None):
        if pt == None:
            pt = self.head_Pos

        is_Collision_Border = pt[0] < 0 or pt[0] >= self.screen_width or pt[1] < 0 or pt[1] >= self.screen_height
        is_Collision_Body = pt in self.body_positions[1:]

        if  is_Collision_Body or is_Collision_Border or self.frame_iteration > 100*len(self.body_positions):
            return True
        return False

    def UpdateScore_text(self,font, size):
        self.score_font = pygame.font.SysFont(font, size)
        self.text_surface = self.score_font.render("Score : " + str(self.score), True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (60, 10)
        self.screen.blit(self.text_surface, self.text_rect)

    def Play_Step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

        self.HandleSnakeMove(action)

        self.reward = 0
        if self.GameOver():
            self.reward = -10
            return self.reward,self.GameOver(), self.score

        # Visuals
        self.screen.fill(self.bg_color)
        self.SnakeGrowth(self.reward)
        self.Draw()

        self.UpdateScore_text('times new roman', 20)

        # updating the screen
        pygame.display.flip()
        self.clock.tick(self.speed)

        return self.reward, self.GameOver(), self.score

