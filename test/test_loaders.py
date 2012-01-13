import os
import sys
import random

import pyglet

import crystals
from crystals import loaders
from crystals import entity
from test.helpers import *

class TestImageDict(object):

    def test_init(self):
        for img_dir in ('terrain', 'item', 'character', 'interface'):
            images = loaders.ImageDict(img_dir, res_path=RES_PATH)

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
        self.loader = loaders.WorldLoader(data_path=DATA_PATH,
                                          res_path=RES_PATH)

    def test_init(self):
        assert self.loader.images == {'terrain': None, 'item': None,
                                      'feature': None, 'character': None}
        assert os.path.join(DATA_PATH, 'world') in sys.path

    def test_load_images(self):
        for atype in loaders.ARCHETYPES:
            self.loader.load_images(atype)
            assert isinstance(self.loader.images[atype], loaders.ImageDict)

    def test_load_archetype_args(self):
        archetype_args = self.loader.load_archetype_args('TestRoom1', 'terrain')
        assert all(type(symbol) == str for symbol in archetype_args.iterkeys())

        symbols = ('-', '|', ',', '+')
        names = ('wall', 'towering wall', 'cobbled floor', 'floor-smooth')
        walkables = (False, False, True, True)
                  
        for symbol, name, walkable in zip(symbols, names, walkables):
            entity_ = entity.Entity(**archetype_args[symbol])
            assert isinstance(entity_, entity.Entity)
            assert isinstance(entity_, pyglet.sprite.Sprite)
            assert entity_.name == name
            assert entity_.walkable == walkable

            entity_.batch = self.batch
            entity_.position = [random.randint(200, 400)] * 2

        #self.run_app()

    def test_load_room(self):
        room1 = self.loader.load_room('TestRoom1')
        assert isinstance(room1, crystals.world.Room)
                
    def test_load_world(self):
        world = self.loader.load_world()
        assert isinstance(world, crystals.world.World)


        # rough integrity test for room.grid ---------------------------
        room1 = world['TestRoom1']
        archetype = 'terrain'
        img = loaders.ImageDict(archetype, RES_PATH)
        vwall = entity.Entity(archetype, 'towering wall', False,
                              img['wall-vert-blue'], room1.batch)
        hwall = entity.Entity(archetype, 'wall', False,
                              img['wall-horiz-blue'], room1.batch)
        floora = entity.Entity(archetype, 'cobbled floor', True,
                               img['floor-a-red'], room1.batch)
        floorb = entity.Entity(archetype, 'floor-smooth', True,
                               img['floor-b-red'], room1.batch)

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
