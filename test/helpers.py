"""helper code for the test suite"""
import os.path

import pyglet

RES_PATH = os.path.join('test', 'res')
DATA_PATH = os.path.join('test', 'data')
IMAGE_PATH = os.path.join(RES_PATH, 'image')

class TestCase(object):

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        self.window.close()

    def run_app(self):
        self.window.push_handlers(self)
        pyglet.app.run()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
