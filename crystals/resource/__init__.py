"""tools for loading variable game data and resources"""
import os.path
import sys

import pyglet
from pyglet.gl import *

from crystals.entity import Entity
from crystals.world import Room, World, Portal, TILE_SIZE

PLAYER_CHAR = '@' # atlas char that represents the player
IGNORE_CHAR = '.' # atlas char that represents empty space

RES_PATH = 'res' # default path to game resources
IMG_PATH = RES_PATH + '/img' # default path to game images
WORLD_PATH = RES_PATH + '/world' # default path to game world scripts

# loader for game resources
loader = pyglet.resource.Loader([
    IMG_PATH + '/terrain', IMG_PATH + '/feature', IMG_PATH + '/item',
    IMG_PATH + '/character'], script_home='.')


class AtlasError(Exception):
    """Raised when invalid code is found in the 'atlas.py' world script."""


def load_entity(obj):
    """Return an Entity instance, given an object whose attributes
    describe it.
    """
    image = loader.image(obj.image)
    return Entity(obj.name, obj.walkable, image)


def load_room(name, atlas, entities):
    """Return a Room instance, given its name, object `atlas` describing
    its layout and object `entities` describing its entities.
    """
    layers = []
    for layer in atlas.map:
        layers.append([])
        for row in layer:
            layers[-1].append([])
            for char in row:
                if char == IGNORE_CHAR:
                    if len(layers) is 1:
                        raise AtlasError("'.' character not allowed in " +
                                         "first layer of atlas.map")
                    entity = None
                else:
                    attrobj = getattr(entities, atlas.key[char])
                    entity = load_entity(attrobj)
                layers[-1][-1].append(entity)

    return Room(name, pyglet.graphics.Batch(), layers)


def load_world():
    """Return a World instance compiled from information found in modules
    'atlas.py' and 'entities.py' at `WORLD_PATH`.
    """
    world_path = os.path.normpath(WORLD_PATH)
    sys.path.insert(0, world_path)
    atlas = __import__('atlas')
    entities = __import__('entities')
    sys.path.remove(world_path)

    rooms = {}
    for rname in atlas.ALL:
        ratlas = getattr(atlas, rname)
        rentities = getattr(entities, rname)
        rooms[rname] = load_room(rname, ratlas, rentities)

    portals = []

    return World(rooms, portals, atlas.START)
