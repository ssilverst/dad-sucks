import pyxel
from enum import Enum
from const import *
import random 
from player import Player
from scuttling_thing import Soul, Redbull, Life, Scuttling_Thing
from halo import Halo, Shootie
from utils import get_highscore, save_highscore
import math

class App:
    #########################
    # The class's variables # 
    #########################
    # These variables are for the dialogue with Dad #
    # and tips from the poof of wisdom              #
    intro = True
    DAD_LINES = ["yo LIZZIE! it's ya Daddy!", 
                "so, errr, late night last night with the ghouls and \n---euuuehehghgh----", 
                 "yeah I kinda let some lost souls loose...",
                 "haha your old man slipped up! ---eeeuuuuuurghghhh",
                 "anyways.. well you know what you gotta do", 
                 "so should be spotless in the next 30 minutes?",
                 "alright yea cool. 'know I can always count on you, \nLizzie.", 
                 "oh and uh if you don't do this you'll face eternal \ndamnation",
                 "you know... yada yada yada", 
                 "oh and watch out for those scum angels,",
                 "they got it in their minds that they can \n~~defeat us~~",
                 "BAHAHAHAHAA, well they'll never defeat me.",
                 "... good luck lizzie.",
                 "i'll be watching.", 
                 "...", 
                 "OH.. I think I let a few more angels through the \ncracks... sorry Lizzie", 
                 "uh Lizzie.. you're supposed to AVOID the angels\nThey don't make good friends, trust me.",
                 "Did you hear me, Lizzie? Angel = BAD\nAngel = stay away!", 
                 "Did it hurt when the angel struck you?\nHaha that sounds like a pick up line",
                 "Lizzie... those angels are not here to help you",
                 "Great, now if you die I'm gonna need to call \nthe dog to clean up...",
                 "FLUFFY!!! COME HERE BOY!"]
    WHAT_LINE_IS_IT_ANYWAYS = 0
    POOF_TIPS = ["Your goal is to capture lost souls \nand bring them to the bag of souls.",
                 "Once you are on top of a soul you \ncan grab it by pressing [R]",
                 "You can only carry three souls at a \ntime so you will want to drop them \noff in the bag by pressing [T]",
                 "Remember: R for grab, T for drop in \nbag, and avoid the angels' shots.",
                 "Red lives are bad. They will take \nback the lost souls from your \nbag if you grab them.",
                 "The magic vials will give you \n!speed! if you pick them up."]
    
    # bools determine whether to flash signal to check tips #
    # if you haven't seen lives or redbulls before then the #
    # poof of wisdom will flash a signal                    #
    seen_lives = False
    seen_rbs = False
    
    hard_mode = False
    hscolor = 0 # color for high scores at the end

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Dad Sucks!")
        self.reset_game(True)
        pyxel.load("assets/calheart.pyxres")
        pyxel.run(self.update, self.draw)

    # Initializing values to set/reset game state #
    # If we are starting the game for the first   #
    # time we want to see the dialogue from dad   #
    # the beginning.                              #
    def reset_game(self, start_game):
        if start_game:
            self.WHAT_LINE_IS_IT_ANYWAYS = 0
        else:        
            self.WHAT_LINE_IS_IT_ANYWAYS = 14

        # variables for dad dialogue and poof's tips #
        self.dad_sassin = False
        self.line_chosen = False
        self.reading_tips = False
        self.signal_new_tip = True 
        self.first_tip = True
        self.next_tip = False
        self.tip_idx = 0
        self.curr_tip_idx = 3
        self.tip_list_index = 0
        self.tips_list = [3]

        # arrs to keep track of all the objects on #
        # the board                                #
        self.souls = []
        self.halos = []
        self.lives = []
        self.redbulls = []
        self.shooties = []
        # dicts holding arrs of the x coords and y coords of each board piece #
        self.x_s = {"souls": [], "lives": [], "rbs": [], "halos": []}
        self.y_s = {"souls": [], "lives": [], "rbs": [], "halos": []}

        self.player = None
        self.dash_timer = 0
        self.dialogue_timer = 0
        
        self.played_death_music = False
        self.played_lobby_music = False 
        self.played_dad_music = False
        self.played_game_music = False
        if self.hard_mode:
            self.highscore = get_highscore(HARD_HIGH_SCORE_FILE)
            self.numHalos = 25
            self.MAX_HALOS = 25
        else:
            self.highscore = get_highscore(HIGH_SCORE_FILE)
            self.numHalos = 2
            self.MAX_HALOS = 10
        self.numLives = 0
        self.shootie_speed = 120
        self.dead = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.check_grab(self.souls, "souls")
            self.check_grab(self.lives, "lives")
            self.check_grab(self.redbulls, "rbs")
        if pyxel.btnp(pyxel.KEY_T):
            self.empty_souls()
        if pyxel.btnp(pyxel.KEY_H) and self.dead:
            self.hard_mode = True
            self.reset_game(False)
        if pyxel.btnp(pyxel.KEY_SPACE) and self.dead:
            self.reset_game(False)

    ##########################################
    # CHECK IF SOUL OR REDBULL OR LIFE TAKEN #
    ##########################################
    def check_grab(self, arr, elemtype):
        for elem in arr:
            if self.player.x >= elem.x - 3 and \
                self.player.x <= elem.x + 19 and \
                self.player.y >= elem.y -3 and \
                self.player.y <= elem.y + 19:
                if elemtype == "rbs":
                    # give the player faster movement #
                    # if they are not already moving  #
                    # faster and start the timer for  #
                    # how long the effect lasts       #
                    if not self.player.dash:
                        self.redbulls.remove(elem)
                        self.player.dash = True
                        self.dash_timer = pyxel.frame_count
                elif elemtype == "souls":
                    if self.player.souls < 3:
                        self.souls.remove(elem)
                        self.player.souls += 1
                        self.set_souls()
                elif elemtype == "lives":
                    self.player.score -= 1
                    self.lives.remove(elem)

    #######################
    # EMPTY SOULS ON HAND #
    #######################
    def empty_souls(self):
        if self.player.x > SCREEN_WIDTH // 2 and \
            self.player.x < SCREEN_WIDTH // 2 + 24 and \
            self.player.y > SCREEN_HEIGHT // 2 +0 and \
            self.player.y < SCREEN_HEIGHT // 2 + 24:
            self.player.score = self.player.score + self.player.souls
            self.player.souls = 0

    # helper function to add x and y to the arr holding x, y for elems #
    def add_elem_to_arr(self, elemtype, arr, classtype):
        x, y = self.create_x_y(self.x_s[elemtype], self.y_s[elemtype])
        self.x_s[elemtype].append(x)
        self.y_s[elemtype].append(y)
        elem = classtype(x, y)
        arr.append(elem)

    # helper function to pick new x's and y's that are not on bag
    def create_x_y(self, x_s, y_s):
        x = None
        y = None
        while (x is None or (x<SCREEN_WIDTH // 2 and x > (SCREEN_WIDTH // 2)+48 and x not in self.x_s)):
            x = random.randint(0, 14) * 16 + 8
        while (y is None or (y<SCREEN_WIDTH // 2 and y > (SCREEN_WIDTH // 2)+48 and y not in self.y_s)):
            y = random.randint(4, 14) * 16 + 8
        return x, y

    ################
    # CREATE SOULS #
    ################
    def set_souls(self):
        for i in range(0, 14-len(self.souls)):
            self.add_elem_to_arr("souls", self.souls, Soul)

    ################
    # CREATE HALOS #
    ################
    def set_halos(self):
        for i in range(0, self.MAX_HALOS):
            self.add_elem_to_arr("halos", self.halos, Halo)

    ################
    # CREATE LIVES #
    ################
    def set_lives(self):
        for i in range(0, self.numLives):
            self.add_elem_to_arr("lives", self.lives, Life)

##################################################################################################################

    ####################
    # DRAWING THE GAME #
    ####################
    def draw(self):
        if self.dead:
            self.draw_death()
        elif self.intro:
            self.draw_intro()
        else:
            if not self.played_game_music:
                pyxel.playm(0, loop=True)
                self.played_game_music = True
            self.draw_game()

    def draw_death(self):
        pyxel.cls(7)
        if not self.played_death_music:
            pyxel.stop()
            pyxel.playm(2, loop=False)
            self.played_death_music = True
        elif self.played_death_music and not self.played_lobby_music:
            pyxel.playm(4, loop=True)
            self.played_lobby_music = True
        pyxel.text(SCREEN_WIDTH//2, SCREEN_HEIGHT//4, "ah, nice try Lizzie.\neternal damnation it is!", 0)
        pyxel.text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "press space to try again", 0)
        pyxel.text(SCREEN_WIDTH //2, (SCREEN_HEIGHT * 3) //4, "or... press h for hard mode.", 0)
        if pyxel.frame_count % 300:
            self.hscolor += 1
        pyxel.text(64, SCREEN_MARGIN, f"easy highscore: {get_highscore(HIGH_SCORE_FILE)}", (self.hscolor % 15))
        pyxel.text(64, SCREEN_MARGIN+16, f"hard highscore: {get_highscore(HARD_HIGH_SCORE_FILE)}", ((15-self.hscolor) % 15))
    #####################################
    # INTRO
    # Dad talking to us @ top of screen # 
    #####################################
    def draw_intro(self):
        pyxel.cls(3)
        if not self.played_dad_music:
            self.played_dad_music = True
            pyxel.playm(3, loop=True)
        pyxel.rect(0, 0, SCREEN_WIDTH, 48, 0)
        pyxel.blt(SCREEN_MARGIN, SCREEN_MARGIN, 0, DAD[0], DAD[1], 32, 32, 0)
        pyxel.text(48, SCREEN_MARGIN, self.DAD_LINES[self.WHAT_LINE_IS_IT_ANYWAYS], 7)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.WHAT_LINE_IS_IT_ANYWAYS = self.WHAT_LINE_IS_IT_ANYWAYS + 1
            if self.WHAT_LINE_IS_IT_ANYWAYS > 13:
                self.intro = False

    def draw_game(self):
        pyxel.cls(3)
        #####################################
        # Dad talking to us @ top of screen # 
        #####################################
        pyxel.rect(0, 0, SCREEN_WIDTH, 48, 0)
        pyxel.blt(SCREEN_MARGIN, SCREEN_MARGIN, 0, DAD[0], DAD[1], 32, 32, 0)
        line_to_say = self.WHAT_LINE_IS_IT_ANYWAYS
        # if player is hit by shootie, then dad sasses. #
        # we pick from options and display the sass for #
        # ~200 frames                                   #
        if self.dad_sassin:
            if self.line_chosen:
                if self.dialogue_timer == 0:
                    self.dialogue_timer = pyxel.frame_count
                elif pyxel.frame_count - self.dialogue_timer > 200:
                    # special case where dad sass is 2 lines #
                    if self.DAD_LINE == 20:
                        self.DAD_LINE = 21
                        self.dialogue_timer = 0
                    else:
                        self.DAD_LINE = 14
                        self.dad_sassin = False
                        self.line_chosen = False
                        self.dialogue_timer = 0
            else:
                self.DAD_LINE = random.randint(17, 20)
                self.line_chosen = True
            line_to_say = self.DAD_LINE
        pyxel.text(48, SCREEN_MARGIN, self.DAD_LINES[line_to_say], 7)

        #####################################
        # GAMEPLAY
        # DRAWING THE OBJECTS AND PLAYER 
        # IN GAME 
        #####################################
        
        # DRAW BAG OF SOULS AND THE POOF OF WISDOM #
        pyxel.blt(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, BAG_A_SOULS[0], BAG_A_SOULS[1], 32, 32, 0)
        pyxel.blt(SCREEN_WIDTH-SCREEN_MARGIN-32, 24, 0, POOF[0], POOF[1], 32, 16, 0)
        
        if (self.signal_new_tip):
            pyxel.blt(SCREEN_WIDTH-SCREEN_MARGIN-27, 16, 0, FULL[0], FULL[1],16, 16, 0)
        
        # DRAW PLAYER #
        if self.player is None: 
            self.player = Player(SCREEN_WIDTH // 2, 24)
            if self.hard_mode:
                self.player.move = 4
                self.player.pitchforks = 5
        if self.player.dash and ((pyxel.frame_count - self.dash_timer) > DASH_TIME) :
            self.player.dash = False
        self.player.draw()
        self.player.update()

        if self.player.souls == 3:
            pyxel.blt(self.player.x, self.player.y-8, 0, FULL[0], FULL[1], 16, 16, 0)
        
        ################
        # UPDATE LEVEL #
        ################
        if not self.hard_mode:
            if self.player.score > 10:
                self.numLives = 3
            if self.player.score > 20:
                self.numHalos = 3
                self.numLives = 7
            elif self.player.score > 50:
                self.numHalos = 5
                self.numLives = 10

        ################
        # INSTRUCTIONS #
        # AND TIPS     # 
        ################
        if (self.player.x >= (SCREEN_WIDTH // 2)) and \
            (self.player.x <= (SCREEN_WIDTH // 2) + 32) and \
            (self.player.y >= SCREEN_HEIGHT // 2) and \
            (self.player.y <= SCREEN_HEIGHT // 2 + 32):
            pyxel.text(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2)+34, "Bag of souls!\noooooh", 10)

        # Creating tips list based on what's out on the board # 
        # You read tips list if not the first instructions    #
        if (not self.seen_lives and not self.lives == []) or \
            (not self.seen_rbs and not self.redbulls == []):
            self.signal_new_tip = True
            if not self.lives == [] and (4 not in self.tips_list):
                self.tips_list.insert(0, 4)
            if not self.redbulls == [] and (5 not in self.tips_list):
                self.tips_list.insert(0, 5)
        if (self.player.x <= SCREEN_WIDTH-SCREEN_MARGIN and \
            self.player.x >= SCREEN_WIDTH-SCREEN_MARGIN-32 and \
            self.player.y >= 16 and \
            self.player.y <= 32):
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reading_tips = True
                self.next_tip = True
            # This means you are reading tips and not introduction to poof #
            if self.reading_tips:
                if self.next_tip:
                    # This is first instructions #
                    if self.first_tip:
                        if self.tip_idx > 2:
                            self.first_tip = False
                            self.signal_new_tip = False
                            self.tip_idx = 0
                            self.curr_tip_idx = self.tip_idx
                        else: 
                            self.curr_tip_idx = self.tip_idx
                            self.tip_idx = self.tip_idx + 1
                    # When poof gets new tips then we display the tips list #
                    else:
                        if self.signal_new_tip:
                            if not self.seen_lives and not self.lives == []:
                                self.seen_lives = True
                                self.signal_new_tip = False
                            if not self.seen_rbs and not self.redbulls == []:
                                self.seen_rbs = True
                                self.signal_new_tip = False
                        self.curr_tip_idx = self.tips_list[self.tip_idx % len(self.tips_list)]
                        self.tip_idx = self.tip_idx + 1
                    self.next_tip = False
                pyxel.text(64, 24, self.POOF_TIPS[self.curr_tip_idx], 10)
            # introduction to poof #
            else:
                pyxel.text(64, 24, "I am the poof of wisdom!", 10)
                pyxel.text(64, 32, "Press [space] to hear my tips.\nI will signal when I get new ones.", 10)
        else:
            self.tip_idx = 0
            self.reading_tips = False
            
        ##############
        # DRAW SOULS #
        ##############
        if len(self.souls) < 14:
            self.set_souls()
        else:
            for soul in self.souls:
                soul.draw()
        # DRAW NET TO CATCH SOULS #
        if pyxel.btn(pyxel.KEY_R):
            pyxel.blt(self.player.x-8, self.player.y, 0, NET[0], NET[1], 16, 16, 0)
        # DRAW LIVES # 
        if len(self.lives) < self.numLives:
            self.set_lives()
        else:
            for life in self.lives:
                life.draw()
        # DRAW HALOS #
        if len(self.halos) == 0:
            self.set_halos()
        else:
            for i in range(0, self.numHalos):
                self.halos[i].draw()

        # DRAW RED BULL # 
        if (pyxel.frame_count % 100 == 0):
            will_redbull = random.randint(0, 100)
            if will_redbull > 85 and len(self.redbulls) < 5: 
                self.add_elem_to_arr("rbs", self.redbulls, Redbull)
        for redbull in self.redbulls:
            redbull.draw()

        ####################
        # ITS SHOOTIE TIME #
        ####################

        # (SHOOTIES ARE THE BLUE BALLS THAT SHOOT OUT OF HALOS) #

        # DRAW SHOOTIES # 
        if (pyxel.frame_count % self.shootie_speed==0):
            for i in range(0, self.numHalos):
                diff_x = self.player.x-self.halos[i].x
                diff_y = self.player.y-self.halos[i].y
                shootie_move_x = 0 if (diff_x == 0) else (diff_x)/abs(diff_x)
                shootie_move_y = diff_y/abs(diff_y) if (diff_x == 0) else (diff_y)/(diff_x)
                shootie = Shootie(self.halos[i], shootie_move_x, shootie_move_y)
                self.shooties.append(shootie)
                shootie.draw()
    
        # UPDATE SHOOTIE POS # 
        for shootie in self.shooties:
            shootie.draw()
            if shootie.x <= self.player.x + 12 and \
                shootie.x >= self.player.x + 4 and \
                shootie.y <= self.player.y + 12 and \
                shootie.y >= self.player.y + 4:
                self.shooties.remove(shootie)
                if self.player.pitchforks > 1:
                    self.player.pitchforks = self.player.pitchforks - 1
                    self.dad_sassin = True
                else: 
                    pyxel.playm(2, loop=False)
                    self.dead = True
                    self.hard_mode = False
            # if shootie goes off bounds it dies # 
            if shootie.x <= 0 or \
                shootie.x >= SCREEN_WIDTH or \
                shootie.y <= 48 or \
                shootie.y >= SCREEN_HEIGHT:
                self.shooties.remove(shootie)

        # DRAW SCORE #
        pyxel.text(SCREEN_WIDTH//2-16, 50, "SCORE: {:02}".format(self.player.score), 13)
        if (self.player.score > self.highscore):
            self.highscore = self.player.score
            if self.hard_mode:
                save_highscore(HARD_HIGH_SCORE_FILE, self.highscore)
            else:
                save_highscore(HIGH_SCORE_FILE, self.highscore)
        pyxel.text(SCREEN_MARGIN, 50, "HIGHSCORE: {:02}".format(self.highscore), 13)

        # DRAW PITCHFORKS #
        h_shift = 16
        for i in range(self.player.pitchforks):
            pyxel.blt(SCREEN_WIDTH-h_shift-SCREEN_MARGIN, SCREEN_MARGIN+36, 0, PITCHFORK[0], PITCHFORK[1], 16, 16, 0)
            h_shift = h_shift + 16
App()