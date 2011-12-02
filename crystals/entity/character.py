"""character.py - intelligent entities that interact with the world"""

from .entity import Entity

ATTRS = ['str', 'end', 'agl', 'dex', 'wil', 'int']
MIN_ATTRS = dict((a, 1) for a in ATTRS)
MAX_ATTRS = dict((a, 99) for a in ATTRS)

MAX_LIFE = 99
MIN_ENERGY = 99

MAX_inventory = 10

class Character(Entity):
    """An intelligent Entity."""

    def __init__(self, name, image, x_range=-1, y_range=-1, interactions=[],
            level=1, attrs=MIN_ATTRS, life=MAX_LIFE, energy=MIN_ENERGY,
            inventory=[], team=None, group=None):
        super(Character, self).__init__(name, False, image, group,
            interactions, x_range=x_range, y_range=y_range)
        
        self._level = level
        self._attrs = attrs
        self._life = life
        self._energy = energy
        self._inventory = inventory

        self._xdir = 1
        self._ydir = 0

    def __str__(self):
        return 'Character' 

    @property
    def level(self):
        return self._level

    @property
    def life(self):
        return self._life

    @property
    def energy(self):
        return self._energy

    @property
    def inventory(self):
        return self._inventory

    @property
    def x_range(self):
        return self._x_range

    @property
    def y_range(self):
        return self._y_range

    def is_alive(self):
        return self.life > 0

    @property 
    def direction(self):
        return self._xdir, self._ydir

    def set_direction(self, xdir, ydir):
        self._xdir = xdir
        self._ydir = ydir

    def get_attr(self, attr=None):
        if not attr:
            return self._attrs.copy()
        return self._attrs[attr]

    def mod_attr(self, attr, num):
        if 1 > self._attrs[attr] + num > MAX_ATTRS:
            return False
        self._attrs[attr] += num
        return True
    
    def mod_life(self, num):
        if not (0 < self._life + num < MAX_LIFE):
            return False
        self._life += num
        return True

    def add_item(self, item):
        if len(self._inventory) >= MAX_inventory:
            return False
        self._inventory.append(item)
        return True

    def remove_item(self, item):
        self._inventory.remove(item)

class Hero(Character):

    def __init__(self, image):
        super(Hero, self).__init__('hero', image)
