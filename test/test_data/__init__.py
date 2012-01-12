import os
import random

import pyglet

from crystals import data
from crystals import entity
from crystals import world
from test.helpers import *

class TestImageDict(object):

    def test_init(self):
        for img_dir in ('terrain', 'item', 'character', 'interface'):
            images = data.ImageDict(img_dir, res_path=RES_PATH)

            filenames = os.listdir(
                os.path.join(RES_PATH, 'image', img_dir))
            assert len(images) == len(filenames)

            # Test that each file in img_dir is represented by an entry
            # in `ImageLoader`
            for key, image in images.iteritems():
                assert isinstance(image, pyglet.image.AbstractImage)
                match = False
                for filename in filenames:
                    if key == filename.rsplit('.', 1)[0]:
                        match = True
                assert match


class TestWorldLoader(TestCase):

    def setup(self):
        super(TestWorldLoader, self).setup()
        self.loader = data.WorldLoader(self.batch, res_path=RES_PATH)

    def test_init(self):
        assert self.loader.images == {'terrain': None, 'item': None,
                                      'character': None}

    def test_load_images(self):
        for etype in data.ENTITY_TYPES:
            self.loader.load_images(etype)
            assert isinstance(self.loader.images[etype], data.ImageDict)

    def test_load_entities(self):
        entity_args = self.loader.load_entity_args('TestRoom', 'terrain')
        assert all(type(symbol) == str for symbol in entity_args.iterkeys())

        symbols = ('-', '|', ',', '+')
        names = ('wall', 'towering wall', 'cobbled floor', 'floor-smooth')
        walkables = (False, False, True, True)
                  
        for symbol, name, walkable in zip(symbols, names, walkables):
            entity_ = entity.Entity(**entity_args[symbol])
            assert isinstance(entity_, entity.Entity)
            assert isinstance(entity_, pyglet.sprite.Sprite)
            assert entity_.name == name
            assert entity_.walkable == walkable

            entity_.batch = self.batch
            entity_.position = [random.randint(200, 400)] * 2

        #self.run_app()

    def test_load_room(self):
        room1 = self.loader.load_room('TestRoom')
        assert isinstance(room1, world.Room)
        assert room1.batch == self.batch

        # rough integrity test for room.grid ---------------------------
        img = data.ImageDict('terrain')
        vwall = entity.Entity('towering wall', False, img['wall-vert-blue'])
        hwall = entity.Entity('wall', False, img['wall-horiz-blue'])
        floora = entity.Entity('cobbled floor', True, img['floor-a-blue'])
        floorb = entity.Entity('floor-smooth', True, img['floor-b-blue'])

        room2 = [
            [[vwall, hwall, vwall],
             [vwall, floorb, vwall],
             [vwall, floorb, floorb]
            ],
            [[floora, floora, floora],
             [floora, None, floora],
             [floora, None, None]]]

        for layer1, layer2 in zip(room1, room2):
            for row1, row2 in zip(layer1, layer2):
                for e1, e2 in zip(row1, row2):
                    if e1 == None:
                        assert e2 == None
                    else:
                        assert e1.name == e2.name
                        assert e1.walkable == e2.walkable
                        assert e1.batch == e2.batch
                
    def test_load_world(self):
        self.loader.load_world()
