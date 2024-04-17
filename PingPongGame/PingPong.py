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
    def __init__(self, screen, radius, center, color, speed):
        self.screen = screen
        self.center = np.array(center, dtype=float)  # Use floating-point coordinates
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction = np.array([1, 1], dtype=float)  # Initial direction vector
        self.score1 = 0
        self.score2 =0

    def draw_circle(self):
        pygame.draw.circle(self.screen, self.color, (int(self.center[0]), int(self.center[1])), self.radius)

    def MoveBall(self, screen_width, screen_height, player1, player2):

        isPlayer1Collision = self.rect_circle_collision(player1)
        isPlayer2Collision = self.rect_circle_collision(player2)

        if isPlayer1Collision or isPlayer2Collision:
            self.ChageDirection(-1,1)
        if self.center[1] - self.radius < 0 or self.center[1] + self.radius > screen_height:
            self.ChageDirection(1,-1)



        if  self.center[0] + self.radius < 0 :
            self.center[0] = screen_width//2
            self.center[1] = screen_height//2
            self.ChageDirection(random.choice([1, -1]), random.choice([1, -1]))
            self.score2 +=1
        if  self.center[0] - self.radius > screen_width:
            self.center[0] = screen_width//2
            self.center[1] = screen_height//2
            self.ChageDirection(random.choice([1, -1]), random.choice([1, -1]))
            self.score1 +=1


        # Update ball position based on speed and direction
        self.center += self.speed * self.direction

    def rect_circle_collision(self, player):
        # Find the closest point on the rectangle to the circle's center
        closest_x = max(player.rect.left, min(self.center[0], player.rect.right))
        closest_y = max(player.rect.top, min(self.center[1], player.rect.bottom))

        # Calculate the distance between the closest point and the circle's center
        distance = math.sqrt((closest_x - self.center[0]) ** 2 + (closest_y - self.center[1]) ** 2)

        # Check if the distance is less than or equal to the circle's radius
        return distance < self.radius

    def ChageDirection(self, xFactor, yFactor):
        self.direction[0] *= xFactor
        self.direction[1] *= yFactor


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
        self.player1 = Padel(self.screen, 15, 120, 15, 100, WHITE, 5)
        self.player2 = Padel(self.screen, 15, 120, self.screen_width-30, 100, WHITE, 5)
        self.ball = Ball(self.screen,10, [self.screen_width//2,self.screen_height//2],WHITE,4)
        self.move_up_P1 = False
        self.move_down_P1 = False
        self.move_up_P2 = False
        self.move_down_P2 = False


    def Draw(self):
        self.player1.draw()
        self.player2.draw()
        self.ball.draw_circle()

    def GameOver(self, pt=None):
        if pt == None:
            pt = self.head_Pos

        is_Collision_Border = pt[0] < 0 or pt[0] >= self.screen_width or pt[1] < 0 or pt[1] >= self.screen_height
        is_Collision_Body = pt in self.body_positions[1:]

        if  is_Collision_Body or is_Collision_Border or self.frame_iteration > 100*len(self.body_positions):
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

        if self.move_down_P2:
            self.player2.move(0, self.player2.speed, self.screen_height)
        if self.move_up_P2:
            self.player2.move(0, -self.player2.speed, self.screen_height)

    def player1_EventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.move_down_P1 = True
            elif event.key == pygame.K_UP:
                self.move_up_P1 = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.move_down_P1 = False
            elif event.key == pygame.K_UP:
                self.move_up_P1 = False

    def player2_EventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.move_down_P2 = True
            elif event.key == pygame.K_w:
                self.move_up_P2 = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.move_down_P2 = False
            elif event.key == pygame.K_w:
                self.move_up_P2 = False

    def Play_Step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            self.player1_EventHandler(event)
            self.player2_EventHandler(event)


        self.ball.MoveBall(self.screen_width,self.screen_height, self.player1, self.player2)

        # Update player position based on movement flags
        self.update_player_position()



        # Draw objects
        self.screen.fill(self.bg_color)
        self.Draw()
        self.UpdateScore_text("Arial", 20, self.ball.score1, (60, 20))
        self.UpdateScore_text("Arial", 20, self.ball.score2, (self.screen_width - 100, 20))

        # Update screen
        pygame.display.flip()
        self.clock.tick(self.FPS)










game = PingPongGame()

while True:
    game.Play_Step()

pygame.quit()