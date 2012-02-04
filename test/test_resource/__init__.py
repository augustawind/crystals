import os
import sys

import pyglet
from nose.tools import *

from crystals import resource
from crystals.world import Room
from crystals.entity import Entity
from test.util import *


@raises(resource.AtlasError)
def TestAtlasError():
    raise resource.AtlasError()


def TestLoadEntity_ValidArgsGiven_ReturnExpectedEntity():
    class AnEntity:
        name = 'guido'
        walkable = False
        image = 'human-peasant.png'
    entity = resource.load_entity(AnEntity)

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
        class cow:
            name = 'cow'
            walkable = False
            image = 'cow.png'
        class sack:
            name = 'sack'
            walkable = True
            image = 'sack.png'

    room = resource.load_room(name, atlas, entities)
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

    room = resource.load_room(name, atlas, entities)


def TestLoadWorld():
    world = resource.load_world()

    assert len(world) is 1
    assert 'RedRoom' in world

    room = world['RedRoom']
    assert isinstance(room, Room)
    assert room.name == 'RedRoom'
    assert len(room) == 2 # depth
    assert len(room[0]) == 5 # height
    assert len(room[0][0]) == 5 # width
