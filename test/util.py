"""utility functions and classes for the test suite"""
import os.path
import os

import pyglet

RES_PATH = 'test/res'
WORLD_PATH = RES_PATH + '/world'
PLOT_PATH = RES_PATH + '/plot'
IMG_PATH = RES_PATH + '/img'

pyglet.resource.path = [
    IMG_PATH + '/terrain', IMG_PATH + '/item', IMG_PATH + '/character']
pyglet.resource._default_loader._script_home = '.'
pyglet.resource.reindex()


class PygletTestCase(object):

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        self.window.close()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
