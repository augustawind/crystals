from nose.tools import *
import pyglet

from crystals import gui

class TestGui(object):

    def setup(self):
        self.window = pyglet.window.Window(200, 200)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        pyglet.app.exit()
        del self.window
        del self.batch

    def test_draw_box(self):
        box = gui.draw_box(0, 0, 10, 10, self.batch)
        assert isinstance(box, pyglet.graphics.vertexdomain.VertexList)
        box.delete()


class TestMenu(TestGui):

    def setup(self):
        TestGui.setup(self)
        self.menu = gui.Menu(0, 0, 50, 50, self.batch,
                            ['t1', 't2', 't3'],
                            [lambda: None for i in range(3)])

    def test_init(self):
        assert isinstance(self.menu, gui.Menu)
        assert self.menu.x == 0
        assert self.menu.y == 0
        assert self.menu.width == 50
        assert self.menu.height == 50
        assert self.menu.batch == self.batch
        assert len(self.menu.text) == 3
        assert len(self.menu.functions) == 3

        assert (self.menu.box.__class__ ==
                gui.draw_box(0, 0, 0, 0, self.batch).__class__)
