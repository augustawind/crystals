"""utility functions and classes for the test suite"""
import os.path
import os

import pyglet

RES_PATH = 'test/res'
WORLD_PATH = RES_PATH + '/world'
PLOT_PATH = RES_PATH + '/plot'
IMG_PATH = RES_PATH + '/img'


class PygletTestCase(object):

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        self.window.close()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
