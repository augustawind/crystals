from collections import namedtuple

from crystals.world.action import *


# Define entity base class
ent = namedtuple('entity', 'name walkable image actions')

# Define the player entity
PLAYER = ent('player', False, 'hero-prophet.png', [])


# Define entities for each room
# ----------------------------------------------------------------------

class Home:

    ALL = ('floor', 'rug', 'vwall', 'hwall', 'hwall_frame', 'table',
           'chair_left', 'chair_right', 'bookcase', 'dad')

    floor = ent('floor tile', True, 'floor-b-brown.png', [])
    rug = ent('rug', True, 'floor-rug-b.png', [])
    vwall = ent('wall', False, 'wall-vert-blue.png', [])
    hwall = ent('wall', False, 'wall-horiz-blue.png', [])
    hwall_frame = ent('frame', False, 'wall-frame-grey.png', [
                      Alert('You see a picture of your family ' +
                            'playing music together.')])

    table = ent('table', False, 'table.png', [])
    chair_left = ent('chair', True, 'chair-left.png', [])
    chair_right = ent('chair', True, 'chair-right.png', [])
    bookcase = ent('bookcase', False, 'bookcase.png', [])

    dad = ent('Dad', False, 'human-warden.png', [
              Talk("My child! It's good to see you in health. Go run " +
                   "along and play now!"),
              UpdatePlot({'CheckDad': True})])
