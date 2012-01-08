"""tools for loading game resources"""
import os

import pyglet

PATH = os.path.join('crystals', 'data') # path to game resources

class ImageDict(dict):
    """Loads game images."""

    def __init__(self, img_dir):
        """Load all images in `img_dir`, where `img_dir` is a
        directory in data/images.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'human-peasant'
        for 'human-peasant.png'.
        """
        path = os.path.join(PATH, 'image', img_dir)
        for filename in os.listdir(path):
            key = filename.rsplit('.', 1)[0]
            image = pyglet.image.load(os.path.join(path, filename))
            self[key] = image


class WorldLoader(object):

    def __init__(self):
        pass
