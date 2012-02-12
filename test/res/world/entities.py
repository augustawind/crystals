from collections import namedtuple

from crystals.world.entity import *

# Define the player entity
PLAYER = Entity('player', False, 'human-peasant.png')


# Define some template entities
class Rfloor(Entity):

    def __init__(self, imgend, actions=[]):
        Entity.__init__(
            self, 'rough surface', True, 'floor-a-' + imgend, actions=actions)

class Sfloor(Entity):

    def __init__(self, imgend, actions=[]):
        Entity.__init__(
            self, 'smooth surface', True, 'floor-b-' + imgend, actions=actions)

class Vwall(Entity):

    def __init__(self, imgend, actions=[]):
        Entity.__init__(
            self, 'wall', False, 'wall-vert-' + imgend, actions=actions)

class Hwall(Entity):

    def __init__(self, imgend, actions=[]):
        Entity.__init__(
            self, 'wall', False, 'wall-horiz-' + imgend, actions=actions)


# Define entities for each room
# ----------------------------------------------------------------------

class RedRoom:

    ALL = ['rfloor', 'sfloor', 'vwall', 'hwall']

    rfloor = Rfloor('red.png')
    sfloor = Sfloor('red.png')
    vwall = Vwall('blue.png')
    hwall = Hwall('blue.png')

    troll = Entity(
        id='troll',
        name='troll',
        walkable=False,
        image='troll.png',
        actions=(
            Alert('I like shorts'),
            UpdatePlot('CheckTroll')))

class BlueRoom:

    ALL = ['sfloor', 'vwall', 'hwall']

    sfloor = Entity('smooth surface', True, 'tree-dead.png')
    vwall = Vwall('blue.png')
    hwall = Hwall('blue.png')
