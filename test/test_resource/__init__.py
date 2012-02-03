import os
import sys

import pyglet
from nose.tools import *

from crystals import resource
from crystals.entity import Entity
from test.util import *


@raises(resource.ResourceError)
def TestResourceError():
    raise resource.ResourceError()


def TestLoadEntity_ValidArgsGiven_ReturnEntityWithExpectedAttrs():
    name = 'george'
    walkable = False
    img = 'human-peasant.png'
    entity = resource.load_entity(name, walkable, img)

    assert entity.name == name
    assert entity.walkable == walkable
    assert isinstance(entity, pyglet.sprite.Sprite)
