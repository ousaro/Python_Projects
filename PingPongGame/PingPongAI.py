import time
import math
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

    def move(self, x_delta, y_delta, screen_height):
        isUpCollision = self.rect.y < 0
        isDownCollison = self.rect.y > screen_height - self.height
        if isUpCollision:
            self.rect.y = 0
        if isDownCollison:
            self.rect.y = screen_height - self.height
        # Move the paddle rectangle in place
        self.rect.y += y_delta


class Ball:
    def __init__(self, screen,width, height, x_pos, y_pos, color, speedX,speedY):
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.color = color
        self.speedX = speedX
        self.speedY = speedY
        self.score1 = 0
        self.score2 =0
        self.reward = 0

    def draw_circle(self):
        pygame.draw.ellipse(self.screen, self.color, self.rect)

    def MoveBall(self, screen_width, screen_height, player1, player2):

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        self.reward = 0
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speedY *= -1

        if self.rect.left <= 0 :
            self.score2 +=1
            self.RespawnBall(screen_width, screen_height)
        if self.rect.right >= screen_width:
            self.score1 +=1
            self.reward = -10
            self.RespawnBall(screen_width, screen_height)

        if self.rect.colliderect(player1) or self.rect.colliderect(player2):
            self.speedX *= -1
        if self.rect.colliderect(player2):
             self.reward = 10

    def RespawnBall(self,screen_width, screen_height):
        self.rect.center = (screen_width//2-10,screen_height//2-10)
        self.speedX = self.speedX * random.choice((-1,1))
        self.speedY = self.speedY * random.choice((-1,1))



class PingPongGame:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600
        self.FPS = 60
        self.bg_color = BLACK
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong Game")
        self.restart()
        self.frame_iteration = 0


    def restart(self):
        self.player1 = Padel(self.screen, 10, 130, 5, 100, WHITE, 5)
        self.player2 = Padel(self.screen, 10, 130, self.screen_width-15, 100, WHITE, 5)
        self.ball = Ball(self.screen,20,20, self.screen_width//2-10,self.screen_height//2-10,WHITE,4,4)
        self.move_up_P1 = False
        self.move_down_P1 = False
        self.playerDirection = "Up"
        self.opponentDirection = "Up"


    def Draw(self):
        self.player1.draw()
        self.player2.draw()
        self.ball.draw_circle()
        pygame.draw.aaline(self.screen,WHITE,(self.screen_width/2,0),(self.screen_width/2,self.screen_height))

    def GameOver(self):
        if self.ball.score1 >= 1:
            return True
        return False

    def UpdateScore_text(self,font, size, score, pos):
        self.score_font = pygame.font.SysFont(font, size)
        self.text_surface = self.score_font.render("Score : " + str(score), True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = pos
        self.screen.blit(self.text_surface, self.text_rect)

    def update_player_position(self):
        if self.move_down_P1:
            self.player1.move(0, self.player1.speed, self.screen_height)
        if self.move_up_P1:
            self.player1.move(0, -self.player1.speed, self.screen_height)

    def player1_EventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.playerDirection = "Down"
                self.move_down_P1 = True
            elif event.key == pygame.K_UP:
                self.playerDirection = "Up"
                self.move_up_P1 = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.move_down_P1 = False
            elif event.key == pygame.K_UP:
                self.move_up_P1 = False

    def HandleOpponentMove(self, action):
        #[up, down]

        if np.array_equal(action,[1,0,0]):#up
            self.opponentDirection = "Up"
            self.player2.move(0,-self.player2.speed, self.screen_height)
        elif np.array_equal(action, [0,1,0]): #Down
            self.opponentDirection = "Down"
            self.player2.move(0,self.player2.speed, self.screen_height)
        else: #not moving [0,0,1]
            self.player2.move(0,0, self.screen_height)




    def Play_Step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.player1_EventHandler(event)

        self.HandleOpponentMove(action)


        self.ball.MoveBall(self.screen_width,self.screen_height, self.player1, self.player2)

        # Update player position based on movement flags
        self.update_player_position()


        if self.GameOver():
            self.ball.reward = -10
            print(f'Player1 score : {self.ball.score1}, Player2 score : {self.ball.score2}')
            return self.ball.reward, self.GameOver(), self.ball.score2


        # Draw objects
        self.screen.fill(self.bg_color)
        self.Draw()
        self.UpdateScore_text("Arial", 20, self.ball.score1, (60, 20))
        self.UpdateScore_text("Arial", 20, self.ball.score2, (self.screen_width - 100, 20))

        # Update screen
        pygame.display.flip()
        self.clock.tick(self.FPS)

        return self.ball.reward, self.GameOver(), self.ball.score2
