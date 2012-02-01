import os
import sys

import pyglet
from nose.tools import *

import crystals
from crystals import data_new as data
from crystals import entity
from test.util import *


@raises(data.ResourceError)
def TestResourceError():
    raise data.ResourceError()


def TestLoadImage():
    data.load_image()


def test_ImageDict():
    for archetype in ('terrain', 'item', 'character', 'interface'):
        images = data.ImageDict(archetype, IMAGE_PATH)

        filenames = os.listdir(os.path.join(IMAGE_PATH, archetype))
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
