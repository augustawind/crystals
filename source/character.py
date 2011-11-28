"""character.py - intelligent entities that interact with the world"""

from world import Entity

ATTRS = ['str', 'end', 'agl', 'dex', 'wil', 'int']
MIN_ATTRS = dict((a, 1) for a in ATTRS)
MAX_ATTRS = dict((a, 99) for a in ATTRS)

MAX_LIFE = 99
MIN_ENERGY = 99

MAX_INV = 10

class Character(Entity):
    """An intelligent Entity."""

    def __init__(self, name, image, interactable, lvl=1, attrs=MIN_ATTRS,
            life=MAX_LIFE, energy=MIN_ENERGY, inv=[], team=None):
        super(Character, self).__init__(name, False, image, interactable)
        
        self.lvl = lvl
        self.attrs = attrs
        self.life = life
        self.energy = energy
        self.inv = inv

        self.dir_x = 1
        self.dir_y = 0

    def __str__(self):
        return 'Character' 

    def get_name(self):
        return self.name

    def get_lvl(self):
        return self.lvl

    def get_attr(self, attr):
        if not attr:
            return self.attrs.copy()
        return self.attrs[attr]

    def mod_attr(self, attr, num):
        if 1 > self.attrs[attr] + num > MAX_ATTRS:
            return False
        self.attrs[attr] += num
        return True

    def get_life(self):
        return self.life
    
    def mod_life(self, num):
        if not (0 < self.life + num < MAX_LIFE):
            return False
        self.life += num
        return True

    def get_energy(self):
        return self.energy

    def get_inv(self):
        return self.inv

    def add_item(self, item):
        if len(self.inv) >= MAX_INV:
            return False
        self.inv.append(item)
        return True

    def remove_item(self, item):
        self.inv.remove(item)

    def get_direction(self):
        return self.dir_x, self.dir_y

    def set_direction(self, x, y):
        self.dir_x = x
        self.dir_y = y

class Hero(Character):

    def __init__(self, image):
        super(Hero, self).__init__('Hero', image, None)
