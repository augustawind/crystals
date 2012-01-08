"""tools for loading game resources"""
import os.path

import pyglet

PATH = os.path.join('crystals', 'data') # path to game resources

class ImageLoader(object):

    def __init__(self):
        self.path = os.path.join(PATH, 'images')
