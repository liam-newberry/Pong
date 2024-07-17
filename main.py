import pygame as pg

from settings import *
from sprites import * 

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()
        self.running = True
    def new(self):
        self.all_sprites = []
        self.now = pg.time.get_ticks()
        self.ball = Ball(self)
        self.all_sprites.append(self.ball)
        self.all_sprites.append(PlayerPaddle(self))
        self.all_sprites.append(CPUPaddle(self))

        self.player_score = 0
        self.cpu_score = 0
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    def update(self):
        self.now = pg.time.get_ticks()
        for sprite in self.all_sprites:
            sprite.update()
    def draw(self):
        self.screen.fill(BLACK)

        for i in range(8):
            pg.draw.rect(self.screen,
                         WHITE,
                         [(WIDTH-10)/2,i*HEIGHT/7.5,10,HEIGHT/15])

        player_score_text = self.draw_text(str(self.player_score),
                                           PLAYER_SCORE_COORDS,
                                           SCORE_PT,
                                           WHITE)
        
        cpu_score_text,s = self.draw_text(str(self.cpu_score),
                                          (0,0),
                                          SCORE_PT,
                                          WHITE,
                                          draw=False)
        cpu_score_text.topright = CPU_SCORE_COORDS
        self.screen.blit(s,cpu_score_text)

        for sprite in self.all_sprites:
            sprite.draw()

        pg.display.flip()
    def draw_text(self,text:str,coordinates:list,pt:int,
                  color:tuple=BLACK,draw:bool=True):
        font = pg.font.Font(FONT,pt)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = coordinates
        if draw:
            self.screen.blit(text_surface,text_rect)
        return text_rect, text_surface


def game_loop():
    g = Game()
    g.new()
    g.run()
game_loop()

pg.quit()