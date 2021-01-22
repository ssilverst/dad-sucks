import pyxel 
from const import *
import random

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move = 2
        self.score = 0
        self.souls = 0
        self.pitchforks = 3
        self.updated = False
        self.icon_x = 0
        self.dash = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.icon_x ,0, 16, 16, 0)
        self.update_icon()
        
    def update_icon(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            if random.randint(0, 100) < 50: self.icon_x = 48
            else: self.icon_x = 64
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if random.randint(0, 100) < 50: self.icon_x = 16
            else: self.icon_x = 32
        elif pyxel.btn(pyxel.KEY_UP): self.icon_x = 80
        elif pyxel.btn(pyxel.KEY_DOWN): self.icon_x = 0

    def check_bounds(self):
        if self.x > SCREEN_WIDTH-SCREEN_MARGIN-16: self.x = SCREEN_WIDTH-SCREEN_MARGIN-16
        elif self.x < SCREEN_MARGIN: self.x = SCREEN_MARGIN
        elif self.y > SCREEN_HEIGHT-SCREEN_MARGIN-16: self.y = SCREEN_HEIGHT-SCREEN_MARGIN-16
        elif self.y < SCREEN_MARGIN: self.y = SCREEN_MARGIN
        
    def update(self):
        move = self.move
        # if pyxel.btnp(pyxel.KEY_SHIFT):
        #     move = random.randint(20, 25)
        if self.dash:
             move = 5
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = self.x - move
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x = self.x + move
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y = self.y + move
        elif pyxel.btn(pyxel.KEY_UP):
            self.y = self.y - move
        
        self.check_bounds()

