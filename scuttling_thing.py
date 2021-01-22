import pyxel
import random
from const import *

class Scuttling_Thing():
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    def update(self):
        # thing will teeter around # 
        x_prob = random.randint(0, 100)
        y_prob = random.randint(0, 100)
        if x_prob < 25: 
            if self.x > -1*SCREEN_MARGIN: self.x = self.x -3
            else: self.x = self.x + 3
        elif x_prob <50: 
            if self.x < SCREEN_WIDTH+SCREEN_MARGIN: self.x = self.x +3
            else: self.x = self.x - 3
        if y_prob < 25: 
            if self.y > 64: self.y = self.y -3
            else: self.y = self.y + 3
        elif y_prob <50: 
            if self.x < SCREEN_HEIGHT+SCREEN_MARGIN: self.y = self.y +3
            else: self.y = self.y - 3

class Soul(Scuttling_Thing):
    def __init__(self, x, y):
        Scuttling_Thing.__init__(self, x, y)
    def draw(self):
        pyxel.blt(self.x, self.y, 0, TORTURED_SOUL[0] ,TORTURED_SOUL[1], 16, 16, 0)
        self.update()
    def update(self):
        Scuttling_Thing.update(self)
        pyxel.blt(self.x, self.y, 0, TORTURED_SOUL[0] ,TORTURED_SOUL[1], 16, 16, 0)
    
class Life:
    def __init__(self, x, y):
        Scuttling_Thing.__init__(self, x, y)
    def draw(self):
        pyxel.blt(self.x, self.y, 0, LIFE[0], LIFE[1], 16, 16, 0)
        self.update()
    def update(self):
        Scuttling_Thing.update(self)
        pyxel.blt(self.x, self.y, 0, LIFE[0] ,LIFE[1], 16, 16, 0)

class Redbull(Scuttling_Thing):
    def __init__(self, x, y):
        Scuttling_Thing.__init__(self, x, y)
    def draw(self):
        pyxel.blt(self.x, self.y, 0, REDBULL[0] ,REDBULL[1], 16, 16, 0)

