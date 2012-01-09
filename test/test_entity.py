import os

import pyglet

from crystals import entity
from test.constants import *

class TestEntity(object):

    def test_init(self):
        image = pyglet.image.load(
            os.path.join(IMAGE_PATH, 'item', 'sack.png'))
        batch = pyglet.graphics.Batch()

        entity_ = entity.Entity('an entity', True, image, batch) 
        assert isinstance(entity_, pyglet.sprite.Sprite)
        assert entity_.image.texture == image.texture
        assert entity_.name == 'an entity'
        assert entity_.walkable == True
        assert entity_.batch == batch
        
        entity_ = entity.Entity('an entity', True, image) 
        assert entity_.batch == None

