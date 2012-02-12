import os
import sys

import pyglet
from nose.tools import *

from crystals import resource
from crystals.world import Room, World, Entity
from test.util import *


def TestScaleImage_ValidParamsGiven_ScaleImage():
    img = pyglet.resource.image('cow.png')
    texture = img.get_texture()

    assert texture.width != 13
    assert texture.height != 13
    resource._scale_texture(img, 13, 13)
    assert texture.width == 13
    assert texture.height == 13


def TestLoadEntity_ValidArgsGiven_ReturnExpectedEntity():
    class AnEntity:
        name = 'guido'
        walkable = False
        image = 'human-peasant.png'
        actions = None
    entity = resource.load_entity(AnEntity)

    assert entity.name == AnEntity.name
    assert entity.walkable == AnEntity.walkable
    assert entity.actions is None


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
                name = getattr(entities, clsname).name
                assert room[ry][x][z].name == name
                walkable = getattr(entities, clsname).walkable
                assert room[ry][x][z].walkable == walkable


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
        class floor:
            name = 'floor'
            walkable = True
            image = 'floor-a-red.png'
            actions = None
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
            actions = None
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'
            actions = None

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
        class floor:
            name = 'floor'
            walkable = True
            image = 'floor-a-red.png'
            actions = None
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
            actions = None
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'
            actions = None

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
