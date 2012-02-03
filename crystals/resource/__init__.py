"""tools for loading variable game data and resources"""
import os
import sys

import pyglet
from pyglet.gl import *

from crystals.entity import Entity
from crystals.world import TILE_SIZE
from crystals.world import Portal
from crystals.world import Room
from crystals.world import World

CHR_PLAYER = '@' # char that represents the player
CHR_IGNORE = '.' # char to ignore when reading maps

RES_PATH = 'res' # default path to game resources
IMG_PATH = RES_PATH + '/img' # default path to game images
WORLD_PATH = RES_PATH + '/world' # default path to game world scripts

# loader for game resources
loader = pyglet.resource.Loader([
    IMG_PATH + '/terrain', IMG_PATH + '/feature', IMG_PATH + '/item',
    IMG_PATH + '/character', WORLD_PATH], script_home='.')


class ResourceError(Exception):
    """Exception class for errors in loading game resources."""


def load_entity(name, walkable, img):
    image = loader.image(img)
    return Entity(name, walkable, image)

#def load_world(self):
    #entities = loader.file('entities.py')
    #atlas = loader.file('atlas.py')
