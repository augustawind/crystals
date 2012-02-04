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
        for y in range(len(atlas.map[z])):
            for x in range(len(atlas.map[z][y])):
                char = atlas.map[z][y][x]

                if char == resource.IGNORE_CHAR:
                    assert room[z][y][x] is None
                    continue

                clsname = atlas.key[char]
                name = getattr(entities, clsname).name
                assert room[z][y][x].name == name
                walkable = getattr(entities, clsname).walkable
                assert room[z][y][x].walkable == walkable


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


def TestLoadWorld_ReturnExpectedWorld():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(world, World)
    assert len(world) is 1
    assert 'RedRoom' in world

    room = world['RedRoom']
    assert isinstance(room, Room)
    assert room.name == 'RedRoom'
    assert len(room[0]) == 5 # Height
    assert len(room[0][0]) == 5 # Width


def TestLoadWorld_ReturnExpectedPlayer():
    world, player = resource.load_world(WORLD_PATH, IMG_PATH)

    assert isinstance(player, Entity)
    assert player.name == 'player'
    assert player.walkable == False

    x, y, z = world.focus.get_coords(player)
    assert x == 2
    assert y == 2
