import os

import pyglet

from crystals import data

class TestImageDict(object):

    def test_init(self):
        for img_dir in ('terrain', 'item', 'character', 'interface'):
            images = data.ImageDict(img_dir)

            filenames = os.listdir(os.path.join(data.PATH, 'image', img_dir))
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


class TestWorldLoader(object):

    def test_init(self):
        loader = data.WorldLoader()
