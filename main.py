import pygame as pg
import sys
from settings import *
from objects import *
from os import path
import pickle
import random
from Generic_Algorithm import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.loops_num = 1

    def load_data(self):
        self.font = path.join("PixelatedRegular-aLKm.ttf")

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.birds = []
        for i in range(TOTAL_POPULATION):
            self.birds.append(Bird((WIDTH//8, HEIGHT//TOTAL_POPULATION*i),27))
        self.birds_backup = []

        self.pipes = []
        self.make_pipes(5)

    def make_pipes(self, num):
        for i in range(5):
            pipe1 = Pipe((WIDTH  + SPACING_HORIZONTAL * i, 0),
                         (100, random.randint(SPACING_VERTICAL, HEIGHT - SPACING_VERTICAL)),i)
            pipe2 = Pipe((WIDTH  + SPACING_HORIZONTAL * i, pipe1.pos.y + pipe1.rect.height + SPACING_VERTICAL),
                         (100, HEIGHT - pipe1.rect.height - SPACING_VERTICAL), i , companion = pipe1)
            self.pipes.append((pipe1, pipe2))

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # for i in range(self.loops_num):
        # kill birds that hit a pipe
        for p_set in self.pipes:
            for n,_ in enumerate(self.birds):
                if p_set[1].rect.colliderect(self.birds[n].rect) or p_set[0].rect.colliderect(self.birds[n].rect) or self.birds[n].hits_bottom():
                    self.birds_backup.append(self.birds[n])
                    self.birds.pop(n)


        if len(self.birds) == 0:
            next_generation(self.birds, self.birds_backup)
            self.pipes = []
            self.make_pipes(5)




        for b in self.birds:
            b.update(self.dt,self.pipes)

        for p_set in self.pipes:
            for p in p_set:
                p.update(self.dt, self.pipes)





    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)
        for b in self.birds:
            b.draw(self.screen)
        for p_set in self.pipes:
            for p in p_set:
                p.draw(self.screen)
        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_s:
                    bird = sorted(self.birds, key= lambda x: x.fitness)[-1]
                    bird.brain.serialize()
                    #print(bird.brain.deserialize().__dict__)
                if event.key == pg.K_m:
                    with open("best_bird.txt", "rb") as f:
                        brain = pickle.load(f)
                    smartest_bird = Bird((WIDTH//8, HEIGHT//2),27, brain = brain)
                    self.birds = [smartest_bird]

            # if event.type == pg.KEYDOWN:
            #     self.loops_num=int(event.unicode)


# create the game object
g = Game()
g.new()
g.run()
