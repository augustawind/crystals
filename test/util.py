"""utility functions and classes for the test suite"""
import os.path
import os

import pyglet

RES_PATH = 'test/res'
IMG_PATH = RES_PATH + '/img'

loader = pyglet.resource.Loader([
    RES_PATH + '/world', IMG_PATH + '/terrain', IMG_PATH + '/feature',
    IMG_PATH + '/item', IMG_PATH + '/character'],
    script_home='.')

def load_image(filename):
    return loader.image(filename)


class PygletTestCase(object):

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        self.window.close()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
