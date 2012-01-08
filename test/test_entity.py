import os

import pyglet

from crystals import entity

DATA_PATH = os.path.join('test', 'data')
IMAGE_PATH = os.path.join(DATA_PATH, 'image')

class TestEntity(object):

    def test_init(self):
        image = pyglet.image.load(
            os.path.join(IMAGE_PATH, 'item', 'sack.png'))
        entity_ = entity.Entity('an entity', True, image) 

        assert entity_.name == 'an entity'
        assert entity_.walkable == True
        assert isinstance(entity_.sprite, pyglet.sprite.Sprite)
