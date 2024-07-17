from math import *
import pygame as pg
from pygame.sprite import Sprite

from settings import *

class Ball(Sprite):
    def __init__(self,game):
        Sprite.__init__(self)
        self.game = game
        self.rect = [WIDTH/2,HEIGHT/2,BALL_SIZE[0],BALL_SIZE[1]]
        self.pos = [self.rect[0],self.rect[1]]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.size = BALL_SIZE
        self.width = BALL_SIZE[0]
        self.height = BALL_SIZE[1]
        self.center = [self.x + self.width/2, self.y + self.height/2]
        self.vel = BALL_SERVE_VEL
        self.vel[0] *= -1
        self.serve_direction = "left"
    def update(self):
        self.bound()
        self.check_score()
        self.pos = [self.x + self.vel[0], self.y + self.vel[1]]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect[0] = self.x
        self.rect[1] = self.y
        self.center = [self.x + self.width/2, self.y + self.height/2]
    def draw(self):
        pg.draw.rect(self.game.screen,WHITE,self.rect)
    def bound(self):
        if not 0 <= self.y <= HEIGHT - self.height:
            self.vel[1] *= -1
    def check_score(self):
        if self.x > WIDTH:
            self.game.player_score += 1
        elif self.x < 0:
            self.game.cpu_score += 1
        else:
            return None
        self.vel = BALL_SERVE_VEL
        if self.serve_direction == "left":
            self.serve_direction = "right"
            self.vel = BALL_SERVE_VEL
        else:
            self.serve_direction = "left"
            self.vel = BALL_SERVE_VEL
            self.vel[0] *= -1
        self.x = (WIDTH + self.width) / 2
        self.y = (HEIGHT + self.height) / 2

class Paddle(Sprite):
    def __init__(self,game):
        Sprite.__init__(self)
        self.game = game
        self.rect = [0,(HEIGHT + PADDLE_SIZE[1])/2,
                     PADDLE_SIZE[0],PADDLE_SIZE[1]]
        self.pos = [self.rect[0],self.rect[1]]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.size = [self.rect[2],self.rect[3]]
        self.width = self.size[0]
        self.height = self.size[1]
        self.center = [self.x + self.width/2, self.y + self.height/2]
        self.bottom = self.y + self.height
        self.vel = [0,0]
        self.last_collision = self.game.now - 200
    def update(self):
        self.pos = [self.x + self.vel[0], self.y + self.vel[1]]
        if self.pos[1] < 0: 
            self.pos[1] = 0
        elif self.pos[1] + self.height > HEIGHT: 
            self.pos[1] = HEIGHT - self.height
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect[0] = self.x
        self.rect[1] = self.y
        self.rect = [self.x,self.y,self.width,self.height]
        self.center = [self.x + self.width/2, self.y + self.height/2]
        self.bottom = self.y + self.height
        self.ball_collide()
    def draw(self):
        pg.draw.rect(self.game.screen,WHITE,self.rect)
    def ball_collide(self):
        ball = self.game.ball
        if ball == None:
            return None
        else:
            if collides(self.rect,ball.rect) and self.game.now - self.last_collision >= 200:
                collide_math(self,ball)
                self.last_collision = self.game.now
        

class CPUPaddle(Paddle):
    def __init__(self,game):
        super().__init__(game)
        self.rect[0] = WIDTH - self.width
        self.pos[0] = self.rect[0]
        self.x = self.pos[0]
        self.center[0] = [self.x + self.width/2]
    def update(self):
        super().update()
        self.move()
        self.rect = [self.x,self.y,PADDLE_SIZE[0],PADDLE_SIZE[1]]
    def move(self):
        ball = self.game.ball
        y_difference = abs(self.y-ball.y)
        if y_difference > 50:
            if ball.center[1] < self.center[1]:
                self.vel = [0,-PADDLE_VEL/2]
            else:
                self.vel = [0,PADDLE_VEL/2]

class PlayerPaddle(Paddle):
    def __init__(self,game):
        super().__init__(game)
    def update(self):
        super().update()
        self.move()
    def move(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_w]:
            self.vel = [0,-PADDLE_VEL]
        elif keystate[pg.K_s]:
            self.vel = [0,PADDLE_VEL]
        else:
            self.vel = [0,0]

def collides(rect1,rect2):
    if len(rect2) == 4:
        rect1_x = rect1[0]
        rect1_y = rect1[1]
        rect1_width = rect1[2]
        rect1_height = rect1[3]
        rect2_x = rect2[0]
        rect2_y = rect2[1]
        rect2_width = rect2[2]
        rect2_height = rect2[3]
        if rect2_x <= rect1_x <= rect2_x + rect2_width:
            if (rect2_y <= rect1_y <= rect2_y + rect2_height or
                rect1_y <= rect2_y <= rect1_y + rect1_height):
                return True
        if rect1_x <= rect2_x <= rect1_x + rect1_width:
            if (rect2_y <= rect1_y <= rect2_y + rect2_height or
                rect1_y <= rect2_y <= rect1_y + rect1_height):
                return True
        return False
    elif len(rect2) == 2:
        rect_x = rect1[0]
        rect_y = rect1[1]
        rect_width = rect1[2]
        rect_height = rect1[3]
        x = rect2[0]
        y = rect2[1]
        if (rect_x <= x <= rect_x + rect_width and
            rect_y <= y <= rect_y + rect_height):
            return True
        return False
    
def collide_math(paddle,ball):
    half_paddle = paddle.height / 2

    x_direction = -1
    if ball.vel[0] < 0:
        x_direction = 1

    
    y_vel = ball.center[1] - paddle.y
    if y_vel < 0:
        y_vel = 0
    if y_vel > half_paddle:
        y_vel -= half_paddle
    else:
        y_vel *= -1
    x_vel = half_paddle - abs(y_vel)

    y_vel = BALL_MAX_VEL * y_vel  / half_paddle
    x_vel = x_direction * abs(BALL_MAX_VEL * x_vel / half_paddle)

    ball.vel = [x_vel,y_vel]