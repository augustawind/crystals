"""utility functions and classes for the test suite"""
import os.path

import pyglet

RES_PATH = os.path.join('test', 'res')
IMAGE_PATH = os.path.join(RES_PATH, 'image')

dummy_image = pyglet.image.load(os.path.join(IMAGE_PATH, 'item', 'sack.png'))


class PygletTestCase(object):

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        self.window.close()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
