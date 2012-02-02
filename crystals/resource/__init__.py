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

RES_PATH = './res' # default path to game resources
PLAYER_CHR = '@' # char that represents the player
IGNORE_CHR = '.' # char to ignore when reading maps
# Parameter names for all entities
ENTITY_PARAMS = ('name', 'archetype', 'walkable', 'image')

pyglet.resource.path = [
    RES_PATH + '/world',
    RES_PATH + '/img/terrain', RES_PATH + '/img/feature',
    RES_PATH + '/img/item', RES_PATH + '/img/character']
pyglet.resource.reindex()


class ResourceError(Exception):
    """Exception class for errors in loading game resources."""
