import os
import sys

import pyglet

from crystals import entity
from crystals.world import action
from test.util import *
from test.test_resource import imgloader

images = imgloader()

class TestEntity(object):

    def TestInit_AttrsHaveExpectedValues(self):
        image = images.image('sack.png')
        batch = pyglet.graphics.Batch()
        actions = [action.Alert(2, 'whoa!', sys.stdout)]

        entity_ = entity.Entity('an entity', True, image, batch,
                                pos=(1, 1), actions=actions) 
        assert isinstance(entity_, pyglet.sprite.Sprite)
        assert entity_.image.texture == image.texture
        assert entity_.name == 'an entity'
        assert entity_.walkable is True
        assert entity_.batch is batch
        assert entity_.pos == (1, 1)
        assert entity_.actions is actions
