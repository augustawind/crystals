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
WORLD_PATH = RES_PATH + '/world' # default path to game world scripts
IMG_PATH = RES_PATH + '/img' # default path to game images

glEnable(GL_TEXTURE_2D)


class AtlasError(Exception):
    """Raised when invalid code is found in the 'atlas.py' world script."""


def _scale_image(img, width, height):
    """Scale `img` to `width` by `height`, keeping pixel sharpness."""
    texture = img.get_texture()
    glBindTexture(GL_TEXTURE_2D, texture.id)
    texture.width = width
    texture.height = height
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def load_entity(obj, imgloader):
    """Return an Entity instance, given an object whose attributes
    describe it.
    """
    image = imgloader.image(obj.image)
    _scale_image(image, TILE_SIZE, TILE_SIZE)
    return Entity(obj.name, obj.walkable, image)


def load_room(name, atlas, entities, imgloader):
    """Return a Room instance, given its name, object `atlas` describing
    its layout and object `entities` describing its entities.
    """
    layers = []
    for layer in atlas.map:
        layers.append([])
        # Read rows in reverse so that maps displayed in symbol form
        # in the atlas mirror the actual appearance of the room
        for row in reversed(layer):
            layers[-1].append([])
            for char in row:
                if char == IGNORE_CHAR:
                    if len(layers) is 1:
                        raise AtlasError("'.' character not allowed in " +
                                         "first layer of atlas.map")
                    entity = None
                else:
                    attrobj = getattr(entities, atlas.key[char])
                    entity = load_entity(attrobj, imgloader)
                layers[-1][-1].append(entity)

    return Room(name, pyglet.graphics.Batch(), layers)


def load_world_scripts(world_path):
    """Return 'atlas.py' and 'entities.py' module objects, given a
    directory that contains those modules.
    """
    world_path = os.path.normpath(world_path)
    sys.path.insert(0, world_path)
    atlas = __import__('atlas')
    entities = __import__('entities')
    sys.path.remove(world_path)
    return atlas, entities


def make_img_loader(img_path):
    return pyglet.resource.Loader([
        img_path + '/terrain', img_path + '/feature', img_path + '/item',
        img_path + '/character'], script_home='.')


def load_world(world_path=WORLD_PATH, img_path=IMG_PATH):
    """Return a World instance and a player Entity instance, compiled
    from information found in modules 'atlas.py' and 'entities.py' at
    `world_path`, and using images at `img_path`.
    """
    # Prepare resources
    atlas, entities = load_world_scripts(world_path)
    imgloader = make_img_loader(img_path)

    # Load rooms
    rooms = {}
    for rname in atlas.ALL:
        ratlas = getattr(atlas, rname)
        rentities = getattr(entities, rname)
        rooms[rname] = load_room(rname, ratlas, rentities, imgloader)

    # Load portals
    portals = []

    # Load world
    world = World(rooms, portals, atlas.START[0])

    # Load and add player to world
    player = load_entity(entities.PLAYER, imgloader)
    rname, rz, ry, rx = atlas.START
    world.add_entity(player, rx, ry, rz, room=world[rname])

    return world, player
