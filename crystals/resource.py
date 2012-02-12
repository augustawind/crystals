"""tools for loading variable game data and resources"""
import os.path
import sys

import pyglet
from pyglet.gl import *

from crystals.plot import Plot
from crystals.world import Room, World, Entity, TILE_SIZE

PLAYER_CHAR = '@' # atlas char that represents the player
IGNORE_CHAR = '.' # atlas char that represents empty space

glEnable(GL_TEXTURE_2D)


def _scale_texture(texture, width, height):
    """Scale `texture` to `width` by `height`, keeping pixel sharpness."""
    glBindTexture(GL_TEXTURE_2D, texture.id)
    texture.width = width
    texture.height = height
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def load_entity(obj):
    """Return an Entity instance, given an object whose attributes
    describe it.
    """
    id = obj.id if hasattr(obj, 'id') else None
    entity = Entity(obj.name, obj.walkable, obj.image, actions=obj.actions,
                    id=id)
    _scale_texture(entity.image, TILE_SIZE, TILE_SIZE)
    return entity


def load_room(name, atlas, entities):
    """Return a Room instance, given its name, object `atlas` describing
    its layout and object `entities` describing its entities.
    """
    grid = []
    # Read rows in reverse so that maps displayed in symbol form
    # in the atlas mirror the actual appearance of the room
    for rows in reversed(zip(*atlas.map)):
        grid.append([])
        for cell in zip(*rows):
            grid[-1].append([])
            for z, char in enumerate(cell):
                if char == IGNORE_CHAR:
                    entity = None
                else:
                    attrobj = getattr(entities, atlas.key[char])
                    entity = load_entity(attrobj)
                grid[-1][-1].append(entity)

    return Room(name, grid)


def load_portals(atlas):
    """Return a list mapping room names to [y][x] indicies indicating
    portal locations and their destination rooms, given object `atlas`
    describing their positions and destination rooms.
    """
    portals = {}
    for y in reversed(xrange(len(atlas.portalmap))):
        for x, char in enumerate(atlas.portalmap[y]):
            if char == IGNORE_CHAR:
                continue
            dest = atlas.portalkey[char]
            portals[dest] = (x, y)

    return portals


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


def load_world(world_path, img_path):
    """Return a World instance and a player Entity instance, compiled
    from information found in modules 'atlas.py' and 'entities.py' at
    `world_path`, and using images at `img_path`.
    """
    # Prepare images
    pyglet.resource.path = [
        img_path + '/terrain', img_path + '/feature', img_path + '/item',
        img_path + '/character']
    pyglet.resource._default_loader._script_home = '.'
    pyglet.resource.reindex()
    assert pyglet.resource._default_loader._script_home == '.'

    # Load world scripts
    atlas, entities = load_world_scripts(world_path)

    # Make rooms and portals
    rooms = {}
    portals = {}
    for rname in atlas.ALL:
        ratlas = getattr(atlas, rname)
        rentities = getattr(entities, rname)
        rooms[rname] = load_room(rname, ratlas, rentities)
        portals[rname] = load_portals(ratlas)

    # Make world
    world = World(rooms, portals, atlas.START[0])

    # Make player character and add to world
    player = load_entity(entities.PLAYER)
    rname, rz, ry, rx = atlas.START
    world.add_entity(player, rx, ry, rz, rname)

    return world, player


def load_plot(plot_path):
    sys.path.insert(0, plot_path)
    triggers = __import__('plot').TRIGGERS
    sys.path.remove(plot_path)

    return Plot(triggers)
