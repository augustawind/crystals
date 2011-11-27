"""combat.py"""

from stats.combat import *

class Battle:

    def __init__(self, game_window):
        self.game_window = game_window

        self.allies = []
        self.enemies = []
        self.rotation = []

    def start(self, allies, enemies):
        self.allies = allies
        self.enemies = enemies

    def start_round(self):
        self.rotation = iter(get_rotation(self.allies + self.enemies))

    def next(self):
        if self.is_battle_over():
            return False

        try:
            actor = self.rotation.next() 
        except StopIteration:
            self.start_round()
            actor = self.rotation.next()
        while not actor.is_alive():
            try:
                actor = self.rotation.next() 
            except StopIteration:
                self.start_round()
                actor = self.rotation.next()

        if actor in self.allies:
            pass # get action from player
        else:
            pass # determine enemy action

        return True

    def is_battle_over(self):
        return bool(self.allies and self.enemies)

    def get_winner(self):
        if not self.enemies:
            winner = self.allies
        else:
            winner = self.enemies

        return winner
