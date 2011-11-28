"""combat.py"""

from stats.combat import *

class Battle:

    def __init__(self, battle_menu):
        self.menu = battle_menu

        self.allies = []
        self.enemies = []
        self.rotation = []

        self.player_actions = {
            'move': self.get_player_movement,
            'attack': self.get_player_target,
            'cast': self.get_player_spell,
            'use': self.get_player_item,
            'crystal': self.get_player_crystal_power}

        self.enemy_actions = {
            'move': self.get_enemy_movement,
            'attack': self.get_enemy_target,
            'cast': self.get_enemy_spell,
            'use': self.get_enemy_item}

        self.actor = None
        self.action = ''

    # player actions ----------------------------------------------------------

    def get_player_action(self):pass

    def get_player_movement(self):pass

    def get_player_target(self):pass

    def get_player_spell(self):pass

    def get_player_item(self):pass

    def get_player_crystal_power(self):pass

    # enemy actions -----------------------------------------------------------

    def get_enemy_action(self):pass

    def get_enemy_movement(self):pass

    def get_enemy_target(self):pass

    def get_enemy_spell(self):pass

    def get_enemy_item(self):pass

    # combat flow logic -------------------------------------------------------

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
            action = self.get_player_action()
            self.player_actions[action]()
        else:
            action = self.get_enemy_action()
            self.enemy_actions[action]()

        return True

    def is_battle_over(self):
        return bool(self.allies and self.enemies)

    def get_winner(self):
        if not self.enemies:
            winner = self.allies
        else:
            winner = self.enemies

        return winner
