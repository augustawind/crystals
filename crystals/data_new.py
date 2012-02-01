"""tools for loading variable game data and resources"""
import os
import sys

import pyglet
from pyglet.gl import *

from crystals import entity
from crystals.world import TILE_SIZE
from crystals.world import Portal
from crystals.world import Room
from crystals.world import World

PATH = 'crystals/res/' # default path to game resources
PLAYER_CHR = '@' # char that represents the player
IGNORE_CHR = '.' # char to ignore when reading maps
# Parameter names for all entities
ENTITY_PARAMS = ('name', 'archetype', 'walkable', 'image')

pyglet.resource.path = [PATH + 'images', PATH + 'world']
pyglet.resource.reindex()

glEnable(GL_TEXTURE_2D)


class ResourceError(Exception):
    """Exception class for errors in loading game resources."""


def load_image(*path):
    """Load an image, given its path relative to 'crystals/res/image'."""
    

class ImageDict(dict):
    """Loads game images."""

    def __init__(self, archetype, path=os.path.join(PATH, 'image')):
        """Load all images in res_path/archetype.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'goblin.png' --> 'goblin'.
        """
        path = os.path.join(path, archetype)
        for filename in os.listdir(path):
            key = os.path.splitext(filename)[0]
            image = pyglet.image.load(os.path.join(path, filename))
            self[key] = image
