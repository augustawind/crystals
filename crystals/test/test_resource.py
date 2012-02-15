import os
import sys
from functools import partial

import pyglet
from nose.tools import *

from crystals import resource
from crystals.world import Room, World, Entity, TILE_SIZE
from crystals.test.util import *


def TestPrepareEntity_ValidParamsGiven_ScaleImage():
    entity = Entity('cow', False, 'cow.png')

    image = entity.image
    assert image.width != TILE_SIZE
    assert image.height != TILE_SIZE
    resource.prepare_sprite(entity)
    assert image.width == TILE_SIZE
    assert image.height == TILE_SIZE


def check_room(room, atlas, entities):
    for z in xrange(len(atlas.map)):
        atlas_y_coords = xrange(len(atlas.map[z]))
        room_y_coords = reversed(atlas_y_coords)
        for ay, ry in zip(atlas_y_coords, room_y_coords):
            for x in xrange(len(atlas.map[z][ay])):
                char = atlas.map[z][ay][x]

                if char == resource.IGNORE_CHAR:
                    assert room[ry][x][z] is None
                    continue

                clsname = atlas.key[char]
                entity = getattr(entities, clsname)()
                assert room[ry][x][z].name == entity.name
                assert room[ry][x][z].walkable == entity.walkable


def TestLoadRoom_ValidArgsGiven_IgnoreCharNotInMap_ReturnExpectedRoom():
    name = 'TestRoom'
    class atlas:
        key = {'+': 'floor', '@': 'cow', 'o': 'sack'}
        map = [
            [
                '+++',
                '+++',
                '+++',
                ],
            [
                'o@o',
                'oo@',
                '@oo']]
    class entities:
        floor = partial(Entity, 
            name = 'floor',
            walkable = True,
            image = 'floor-a-red.png')
        cow = partial(Entity, 
            name = 'cow',
            walkable = False,
            image = 'cow.png')
        sack = partial(Entity, 
            name = 'sack',
            walkable = True,
            image = 'sack.png')

    room = resource.load_room(name, atlas, entities)
    check_room(room, atlas, entities)


def TestLoadRoom_ValidArgsGiven_IgnoreCharInZLevel1_ReturnExpectedRoom():
    name = 'TestRoom'
    class atlas:
        key = {'+': 'floor', '@': 'cow', 'o': 'sack'}
        map = [
            [
                '+++',
                '+++',
                '+++',
                ],
            [
                'o@o',
                'o' + resource.IGNORE_CHAR + '@',
                '@oo']]
    class entities:
        floor = partial(Entity, 
            name = 'floor',
            walkable = True,
            image = 'floor-a-red.png')
        cow = partial(Entity, 
            name = 'cow',
            walkable = False,
            image = 'cow.png')
        sack = partial(Entity, 
            name = 'sack',
            walkable = True,
            image = 'sack.png')

    room = resource.load_room(name, atlas, entities)
    assert room[1][1][1] is None
    check_room(room, atlas, entities)


def TestLoadPortals_LoadExpectedPortals():
    class atlas:
        portalkey = {'1': 'Room1', '2': 'Room2'}
        portalmap = [
            '..2',
            '.1.',
            '...']
    portals = resource.load_portals(atlas)

    assert portals == {'Room1': (1, 1), 'Room2': (2, 0)}


def TestLoadWorld_ReturnExpectedWorld():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(world, World)
    assert len(world) is 2
    assert 'RedRoom' in world
    assert world.focus == world['RedRoom']

    room = world['RedRoom']
    assert isinstance(room, Room)
    assert room.name == 'RedRoom'
    assert len(room) == 5 # Height
    assert len(room[0]) == 5 # Width

    room = world['BlueRoom']
    assert isinstance(room, Room)
    assert room.name == 'BlueRoom'
    assert len(room) == 5
    assert len(room[0]) == 5
    assert len(room[0][0]) == 1


def TestLoadWorld_ReturnExpectedPlayerAtExpectedCoords():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(player, Entity)
    assert player.name == 'player'
    assert player.walkable == False

    x, y, z = world.focus.get_coords(player)
    assert x == 2
    assert y == 2


def TestLoadPlot():
    resource.load_plot(PLOT_PATH)
