import os
import random

import pyglet

from crystals import data
from crystals import entity
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
        self.loader = data.WorldLoader(res_path=RES_PATH)

    def test_init(self):
        assert self.loader.images == {'terrain': None, 'item': None,
                                      'character': None}

    def test_load_images(self):
        for etype in data.ENTITY_TYPES:
            self.loader.load_images(etype)
            assert isinstance(self.loader.images[etype], data.ImageDict)

    def test_load_entity(self):
        entity_ = self.loader.load_entity(
            'an entity', False,
            pyglet.image.load(os.path.join(IMAGE_PATH, 'item', 'sack.png')))
        assert isinstance(entity_, entity.Entity)

    def test_load_entities(self):
        entities = self.loader.load_entities('terrain')
        images = data.ImageDict('terrain', RES_PATH)
        assert all(type(symbol) == str for symbol in entities.iterkeys())
        assert all(isinstance(entity_, entity.Entity)
                   for entity_ in entities.itervalues())

        symbols = ('-', '|', ',', '+')
        names = ('wall', 'towering wall', 'cobbled floor', 'floor-smooth')
        imagedict = data.ImageDict('terrain', RES_PATH)
        images = [imagedict[name] for name in
                    ('wall-horiz-blue', 'wall-vert-blue',
                        'floor-a-red', 'floor-b-red')]
                  
        for symbol, name, image in zip(symbols, names, images):
            assert entities[symbol].name == name
            assert isinstance(entities[symbol], pyglet.sprite.Sprite)

            entities[symbol].batch = self.batch
            entities[symbol].position = [random.randint(200, 400)] * 2

        #self.run_app()
                

    def test_load_world(self):
        self.loader.load_world()
