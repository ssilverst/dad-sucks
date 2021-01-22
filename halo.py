import pyxel
import random
from const import *
class Halo:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move_x = random.choice([-1,1]) 
        self.move_y = random.choice([-1, 1]) 
        self.shooties = []

    def draw(self):
        pyxel.blt(self.x, self.y, 0, HALO[0] ,HALO[1], 16, 16, 0)
        self.update()

    def update(self):
        # halos will move from boundary to boundary # 
        if self.x < SCREEN_MARGIN: self.move_x = 1
        if self.x > SCREEN_WIDTH - SCREEN_MARGIN: self.move_x = -1
        if self.y < 64: self.move_y = 1
        if self.y > SCREEN_HEIGHT-SCREEN_MARGIN: self.move_y = -1
        self.x = self.x + self.move_x
        self.y = self.y + self.move_y
        pyxel.blt(self.x, self.y, 0, HALO[0] ,HALO[1], 16, 16, 0)

class Shootie:
    def __init__(self, halo, move_x, move_y):
        self.x = halo.x
        self.y = halo.y
        self.halo = halo
        self.move_x = move_x
        self.move_y = move_y 

    def draw(self):
        pyxel.rect(self.x, self.y, 5, 5, 6)
        self.update()

    def update(self):
        self.x = self.x + (self.move_x*2)
        self.y = self.y + (self.move_y*2) 
