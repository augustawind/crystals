"""executing and rendering combat"""

from random import random

from stats.combat import *
from world import Room


class CombatGrid(Room):

    def __init__(self, room):
        super(BattleGrid, self).__init__('combat', width=9, height=9) 
        

class Combat(object):

    def __init__(self, menu):
        self.menu = menu

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

    # computations ------------------------------------------------------------

    def get_rotation(self, *characters):
        """Return characters list sorted by agl stat, highest to lowest."""
        return sorted(characters,
            key=lambda x: x.get_attr('agl' + random(), reverse=True))

    def get_damage(self, attacker, defender):
        """Return damage dealt to defender in an attack from attacker."""
        return attacker.get_attr('str') - (defender.get_attr('end') / 2)

    def attack_hits(self, attacker, defender):
        """Return True if attack by attacker hits defender."""
        return ((attacker.get_attr('dex') -
            defender.get_attr('dex') + 75) / 100.0 > random())

    # player actions ----------------------------------------------------------

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
            action = self.menu.get_player_action()
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
