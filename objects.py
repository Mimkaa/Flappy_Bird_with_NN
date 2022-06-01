import pygame as pg
import random
from settings import *
import math
from Neural_Network.objects import NeuralNetwork
vec = pg.Vector2

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)


    # Convert the 0-1 range into a value in the right range.

    return rightMin + (valueScaled * rightSpan)

def distance(vec1, vec2):
    return math.sqrt((vec2.x-vec1.x)**2 + (vec2.y - vec1.y)**2)

class Polygon:
    def __init__(self,pos):
        self.points=[]
        self.pos=vec(pos)
        self.angle=0
        self.originals=[]
        self.overlap=False
    def rotate(self,angle):
        self.angle+=angle

    def move(self,dir):
        vel=vec(math.cos(self.angle),math.sin(self.angle)).normalize()
        vel.scale_to_length(dir)
        self.pos+=vel

    def update(self):
        for n,point in enumerate(self.points):
            self.points[n].x=(self.originals[n].x*math.cos(self.angle)-self.originals[n].y*math.sin(self.angle))+self.pos.x
            self.points[n].y=(self.originals[n].x*math.sin(self.angle)+self.originals[n].y*math.cos(self.angle))+self.pos.y


class Bird:
    def __init__(self, pos, radius, brain = None):
        self.pos = vec(pos)
        self.radius = radius
        self.vel = vec(0, 0)
        self.acc = vec(0, 1800)
        self.rotation_extend = 0
        self.pointer = vec(0,0)
        theta=(math.pi*2)/4
        self.polygon = Polygon((radius//2,radius//2))

        for i in range(4):
            self.polygon.points.append(vec(self.radius*math.cos(theta*i+math.radians(45)),self.radius*math.sin(theta*i+math.radians(45))))
            self.polygon.originals.append(vec(self.radius*math.cos(theta*i+math.radians(45)),self.radius*math.sin(theta*i+math.radians(45))))
        self.polygon.update()
        self.make_new_rect()

        if not brain:
            self.brain = NeuralNetwork(5,10,2)
        else:
            self.brain = brain.copy()
        self.score = 0
        self.fitness = 0


    def make_new_rect(self):
        ys =  [p.y for p in self.polygon.points]
        xs =  [p.x for p in self.polygon.points]
        min_x = min(xs)
        man_x = max(xs)
        min_y = min(ys)
        man_y = max(ys)
        width = man_x - min_x
        height = man_y - min_y
        self.rect = pg.Rect(self.pos.x + width//2,self.pos.y + height//2, width, height)

        self.rect.center = self.pos

    def up(self):
        self.vel += vec(0, -600)

    def mutate(self, percent):
        self.brain.mutate(percent)

    def hits_bottom(self):
        return self.rect.bottom > HEIGHT

    def think(self,pipes):
        closest_pipe_set = [None,None]
        closest_pipe_dist = float('-inf')
        for p_set in pipes:
            d = self.pos.x - p_set[0].pos.x - p_set[0].rect.width
            if (d > closest_pipe_dist) and d < 0:
                closest_pipe_set = [*p_set]
                closest_pipe_dist = self.pos.x - p_set[0].pos.x

        inputs = [self.pos.y/HEIGHT, closest_pipe_set[0].rect.bottomleft[1]/HEIGHT, closest_pipe_set[1].rect.topleft[1]/HEIGHT, abs(closest_pipe_dist/WIDTH), self.vel.y/600 ]

        output = self.brain.predict(inputs)
        # if output[0] > output[1] and self.vel.y >= 0 :
        if output[0] > output[1] :
            self.up()


    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.up()


    def update(self,dt, pipes):
        self.score += 1
        self.think(pipes)
        self.rotation_extend = translate(self.vel.y,-1000, 1000, -1, 1)

        self.pointer = vec(self.pos.x + 100, self.pos.y+distance(self.pos+vec(100,100),self.pos+vec(100,-100))*self.rotation_extend)

        self.vel += self.acc * dt
        self.pos += self.vel * dt

        # update the polygon
        dir_vec = self.pointer - self.pos
        angle = math.atan2(dir_vec.y, dir_vec.x)
        self.polygon.angle = angle

        self.polygon.angle = angle
        self.polygon.update()
        self.make_new_rect()


        if self.pos.y > HEIGHT:
            self.vel *= 0
            self.pos.y = HEIGHT
        elif self.pos.y < 0:
            self.vel *= 0
            self.pos.y = 0

    def find_center_poly(self):
        center = vec(0,0)
        for p in self.polygon.points:
            center += p
        return center/len(self.polygon.points)

    def draw(self, surf):
        new_surf = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)

        offset = vec(self.rect.width//2, self.rect.height//2) - self.find_center_poly()
        new_points = [p + offset for p in self.polygon.points]
        pg.draw.polygon(new_surf,WHITE,new_points)
        pg.draw.polygon(new_surf,BLACK,new_points,1)

        surf.blit(new_surf,vec(self.rect.topleft))
        # pg.draw.line(surf,WHITE,self.pos+vec(100,100), self.pos+vec(100,-100))
        # pg.draw.circle(surf,WHITE,self.pointer, 10)
        #pg.draw.rect(surf,WHITE,self.rect,1)
        #pg.draw.circle(surf, WHITE, self.pos, self.radius)


class Pipe:
    def __init__(self, pos, dimensions, index, companion = None):
        self.pos = vec(pos)
        self.rect = pg.Rect(self.pos.x, self.pos.y, *dimensions)
        self.companion = companion
        self.index = index
    def update(self, dt, all_pipes):
        self.pos += vec(-150*dt, 0)
        self.rect.topleft = self.pos
        if self.pos.x < -self.rect.width :
            self.pos.x = all_pipes[self.index - 1][0].rect.right + SPACING_HORIZONTAL - all_pipes[self.index - 1][0].rect.width
            if self.companion:
                self.rect.height = HEIGHT - self.companion.rect.height - SPACING_VERTICAL
                self.pos.y = self.companion.pos.y + self.companion.rect.height + SPACING_VERTICAL
            else:
                self.rect.height = random.randint(SPACING_VERTICAL, HEIGHT - SPACING_VERTICAL)


    def draw(self, surf):
        pg.draw.rect(surf, WHITE, self.rect)