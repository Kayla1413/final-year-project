# coding:utf-8

import random
import pygame
import os
import time

from player import Player
from interface import Setting, Background, check_events

# H S D C
# Heart Spade Diamond Club

class Game:
    def __init__(self):
        self.cards = None
        self.players = [Player('East'),Player('North'),Player('West'), Player('South')]
        self.loser = 0

    def covert(self, s):
        if s == 1 or s == 14:
            return 'A'
        elif s < 10:
            return str(s)
        elif s == 10:
            return '0'
        elif s == 11:
            return 'J'
        elif s == 12:
            return 'Q'
        elif s == 13:
            return 'K'
        
    # new game initialization
    def new_game(self, background):
        self.loser = -1
        self.player_cards = [[],[],[],[]]

        cards = self.create_card()
        random.shuffle(cards)
        
        # shuffle
        turn = 0
        for i in range(len(cards)):
            x = self.players[turn].add_card(cards[i])
            self.player_cards[turn].append(cards[i])
            background.add_card(cards[i], turn)

            turn += 1
            turn %= 4
           # check_events()

    '''create a set of cards'''
    def create_card(self):
        colors = ['H', 'S', 'D', 'C']
        nums = 'A234567890JQK'
        cards = []
        for color in colors:
            for i in range(13):
                c = color + nums[i]
                cards.append(c)
        return cards

   
    def is_big(self,b, a):
        num_order = ['A', 'K', 'Q', 'J', '0', '9','8','7','6','5','4','3','2']
        for x in num_order:
            if x == a:
                return False
            if x == b:
                return True

    def is_bigger(self,a , b, this_color):
        if a[1] == self.main_num:
            if b == 'jk' or b=='JK' or b[0]==self.main_color and b[1]==self.covert(self.main_num):
                return False
            else:
                return True
        if a[0] == self.main_color:
            if b =='jk' or b=='JK' or b[1]==self.covert(self.main_num) or b[0]==self.main_color and self.is_big(b[1],a[1]):
                return False
            else:
                return True
        if a[0] == this_color:
            if b =='jk' or b=='JK' or b[1]==self.covert(self.main_num) or b[0]==self.main_color or b[0]==this_color and self.is_big(b[1],a[1]):
                return False
            else:
                return True
        
        if b =='jk' or b=='JK' or b[1]==self.covert(self.main_num) or b[0]==self.main_color or b[0]==this_color or self.is_big(b[1],a[1]):
            return False
        else:
            return True

    def is_a_card(self, s):
        if s[0] in ['H', 'S', 'D', 'C'] and s[1] in ['A', 'K', 'Q', 'J', '0', '9','8','7','6','5','4','3','2']:
            return True
        else:
            return False


    def run_game(self, background):
        roles = {'North': 1, 'East':2, 'South':3,'West':0}
        turn = 0

        while(True):
            for role in roles:
                if role == 'North':
                    check_events(flag = 1, background = background, role = roles[role], turn = turn)
                elif role == 'East':
                    background.draw_pass(turn, roles[role])
                elif role == 'South':
                    check_events(flag = 1, background = background, role = roles[role], turn = turn)
                    turn += 1
                    if turn >= 8:
                        return
                else:
                    background.draw_pass(turn, roles[role])
                time.sleep(0.5)
            
            check_events()


        
if __name__ == '__main__':
	# Initialize pygame
    pygame.init()
    setting = Setting()
    SCREEN_WIDTH, SCREEN_HEIGHT = setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT
    x, y = 150, 60
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bridge")
    background = Background(screen, setting)
    game = Game()
    time.sleep(0.5)
    while True:
        check_events()
        game.new_game(background)
        check_events()
        game.run_game(background)
        check_events()
        background.initial()
        check_events()   
        time.sleep(2)
