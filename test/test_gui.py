from nose.tools import *
import pyglet

from crystals import gui

class AbstractTest(object):

    def __init__(self, run_app=False):
        self.run_app = run_app

    def setup(self):
        self.window = pyglet.window.Window(600, 400)
        self.batch = pyglet.graphics.Batch()

    def teardown(self):
        if self.run_app:
            self.window.push_handlers(self)
            pyglet.app.run()
            self.run_app = False
        self.window.close()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()


class TestBox(AbstractTest):

    def __init__(self):
        super(TestBox, self).__init__(run_app=True)

    def setup(self):
        super(TestBox, self).setup()
        self.args = (0, 0, 50, 50, self.batch)
        self.box = gui.Box(*self.args)

    def teardown(self):
        super(TestBox, self).teardown()

    def test_init(self):
        assert isinstance(self.box, gui.Box)
        assert (self.box.x, self.box.y, self.box.width, self.box.height,
                self.box.batch) == self.args
        assert (
            self.box.box is None or
            isinstance(self.box.box, pyglet.graphics.vertexdomain.VertexList))

    def test_show(self):
        self.box.show()
        assert hasattr(self.box, 'vertex_data')
        assert hasattr(self.box, 'color_data')
        assert isinstance(self.box.box,
                          pyglet.graphics.vertexdomain.VertexList)

    def test_hide(self):
        self.box.show()
        self.box.hide()


class TestMenu(AbstractTest):

    def __init__(self):
        super(TestMenu, self).__init__(run_app=True)

    def setup(self):
        super(TestMenu, self).setup()
        self.x, self.y = 0, 0
        self.width, self.height = 300, 300
        self.text = ['Here Lies Text', 'the next text is hexed', 'inTEXTicated']
        self.functions = [lambda: None for i in range(3)]
        self.kwargs = {'box': True}
        self.create_menu()

    def create_menu(self):
        self.menu = gui.Menu(self.x, self.y, self.width, self.height, self.batch,
                             self.text, self.functions, **self.kwargs)

    def teardown(self):
        super(TestMenu, self).teardown()

    def test_init(self):
        assert isinstance(self.menu, gui.Menu)
        assert self.menu.x == self.x
        assert self.menu.y == self.y
        assert self.menu.width == self.width
        assert self.menu.height == self.height
        assert self.menu.batch == self.batch
        assert self.menu.text == self.text
        assert self.menu.functions == self.functions
        assert len(self.menu.functions) == len(self.menu.text)

        assert isinstance(self.menu.box, gui.Box)

        for i in range(len(self.menu.labels)):
            label = self.menu.labels[i]
            assert isinstance(label, pyglet.text.Label)
            assert label.text == self.text[i]
            assert label.font_name == 'monospace'
            assert label.font_size == 16
            assert label.bold == False
            assert label.italic == False
            assert label.color == (255, 255, 255, 255)
            assert label.anchor_x == 'center'
            assert label.anchor_y == 'baseline'
            assert label.multiline == False
            assert label.batch == self.batch

    """def test_select_item(self):
        menu.select_item(1)
        assert 


        assert all([isinstance(box, pyglet.graphics.vertexdomain.VertexList)
                    for box in self.menu.boxes])"""
