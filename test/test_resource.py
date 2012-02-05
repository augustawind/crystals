import os
import sys

import pyglet
from nose.tools import *

from crystals import resource
from crystals.world import Room, World
from crystals.entity import Entity
from test.util import *

RES_PATH = 'test/res'
WORLD_PATH = RES_PATH + '/world'
IMG_PATH = RES_PATH + '/img'


def imgloader():
    return pyglet.resource.Loader([
        IMG_PATH + '/terrain', IMG_PATH + '/feature', IMG_PATH + '/item',
        IMG_PATH + '/character'], script_home='.')


@raises(resource.AtlasError)
def TestAtlasError():
    raise resource.AtlasError()


def TestScaleImage_ValidParamsGiven_ScaleImage():
    img = imgloader().image('cow.png')
    texture = img.get_texture()
    assert texture.width != 13
    assert texture.height != 13

    resource._scale_image(img, 13, 13)
    assert texture.width == 13
    assert texture.height == 13


def TestLoadEntity_ValidArgsGiven_ReturnExpectedEntity():
    class AnEntity:
        name = 'guido'
        walkable = False
        image = 'human-peasant.png'
    entity = resource.load_entity(AnEntity, imgloader())

    assert entity.name == AnEntity.name
    assert entity.walkable == AnEntity.walkable
    assert isinstance(entity, pyglet.sprite.Sprite)


def check_room(room, atlas, entities):
    for z in range(len(atlas.map)):
        atlas_y_coords = range(len(atlas.map[z]))
        room_y_coords = reversed(atlas_y_coords)
        for ay, ry in zip(atlas_y_coords, room_y_coords):
            for x in range(len(atlas.map[z][ay])):
                char = atlas.map[z][ay][x]

                if char == resource.IGNORE_CHAR:
                    assert room[z][ry][x] is None
                    continue

                clsname = atlas.key[char]
                name = getattr(entities, clsname).name
                assert room[z][ry][x].name == name
                walkable = getattr(entities, clsname).walkable
                assert room[z][ry][x].walkable == walkable


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
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'

    room = resource.load_room(name, atlas, entities, imgloader())
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
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'

    room = resource.load_room(name, atlas, entities, imgloader())
    assert room[1][1][1] is None
    check_room(room, atlas, entities)


@raises(resource.AtlasError)
def TestLoadRoom_IgnoreCharInLayer0_RaiseAtlasError():
    name = 'TestRoom'
    class atlas:
        key = {'+': 'floor', '@': 'cow', 'o': 'sack'}
        map = [
            [
                '+++',
                '+.+',
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
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'

    room = resource.load_room(name, atlas, entities, imgloader())


def TestLoadPortals_LoadExpectedPortals():
    class atlas:
        portalkey = {'1': 'Room1', '2': 'Room2'}
        portalmap = [
            '..2',
            '.1.',
            '...']
    portals = resource.load_portals(atlas)

    assert len(portals) == 3 # height
    assert len(portals[0]) == 3 # width
    portal1 = portals[1][1]
    assert portal1 == 'Room1'
    portal2 = portals[2][2]
    assert portal2 == 'Room2'


def TestLoadWorld_ReturnExpectedWorld():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(world, World)
    assert len(world) is 2
    assert 'RedRoom' in world
    assert world.focus == world['RedRoom']

    room = world['RedRoom']
    assert isinstance(room, Room)
    assert room.name == 'RedRoom'
    assert len(room[0]) == 5 # Height
    assert len(room[0][0]) == 5 # Width

    room = world['BlueRoom']
    assert isinstance(room, Room)
    assert room.name == 'BlueRoom'
    assert len(room) == 1
    assert len(room[0]) == 5
    assert len(room[0]) == 5


def TestLoadWorld_ReturnExpectedPlayer():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(player, Entity)
    assert player.name == 'player'
    assert player.walkable == False

    x, y, z = world.focus.get_coords(player)
    assert x == 2
    assert y == 2
