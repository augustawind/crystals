import os

import pyglet

from crystals import entity
from test.constants import *

class TestEntity(object):

    def test_init(self):
        image = pyglet.image.load(
            os.path.join(IMAGE_PATH, 'item', 'sack.png'))
        entity_ = entity.Entity('an entity', True, image) 

        assert entity_.name == 'an entity'
        assert entity_.walkable == True
        assert isinstance(entity_.sprite, pyglet.sprite.Sprite)
        assert entity_.sprite.image.texture == image.texture
