import pygame
import random
import  numpy as np

#initializing the pygame
pygame.init()

#color
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (125,125,125)


class Padel:
    def __init__(self, screen, width, height, x_pos, y_pos, color, speed):
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x_pos, y_pos, width, height)  # Create a rectangle representing the paddle
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)  # Draw the paddle using the rectangle

    def move(self, x_delta, y_delta):
        self.rect.move_ip(x_delta, y_delta)  # Move the paddle rectangle in place


class Ball:
    def __init__(self, radious, xPos, yPos, color, speed):
        self.radious = radious
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
        self.speed = speed
        self.xDirection = 1
        self.yDirection = 1

    def MoveBall(self, x ,y):
        self.xPos += x * self.xDirection
        self.yPos += y * self.yDirection

    def ChageDirection(self, xFactor, yFactor):
        self.xDirection *= xFactor
        self.yDirection *= yFactor


class PingPongGame:
    def __init__(self):
        # init screen
        self.screen_width, self.screen_height = 800, 600
        self.FPS = 60
        self.bg_color = BLACK
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ping Pong Game")
        # init snake
        self.restart()


    def restart(self):
        self.score = 0
        self.player1 = Padel(self.screen, 15, 120, 15, 100, WHITE, 15)


    def Draw(self):
        self.player1.draw()

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

    def Play_Step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Moving the player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.player1.move(0,self.player1.speed)
                if event.key == pygame.K_UP:
                    self.player1.move(0,-self.player1.speed)
                if event.key == pygame.K_LEFT:
                    self.player1.move(-self.player1.speed,0)
                if event.key == pygame.K_RIGHT:
                    self.player1.move(self.player1.speed,0)


        # Draw objects
        self.screen.fill(self.bg_color)
        self.Draw()

        # Update screen
        pygame.display.flip()
        self.clock.tick(self.FPS)










game = PingPongGame()

while True:
    game.Play_Step()

pygame.quit()