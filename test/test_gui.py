from itertools import permutations

from nose.tools import *
import pyglet

from crystals import gui

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


class TestBox(TestCase):

    def setup(self):
        super(TestBox, self).setup()
        self.args = (0, 0, 50, 50, self.batch, gui.COLOR_RED)
        self.box = gui.Box(*self.args)

    def teardown(self):
        super(TestBox, self).teardown()
        self.box.hide()

    def test_init(self):
        assert isinstance(self.box, gui.Box)
        assert (self.box.x, self.box.y, self.box.width, self.box.height,
                self.box.batch, self.box.color) == self.args
        assert (
            self.box.box is None or
            isinstance(self.box.box, pyglet.graphics.vertexdomain.VertexList))

    def test_visible(self):
        assert not self.box.visible
        self.box.show()
        assert self.box.visible

    def test_show(self):
        self.box.show()
        assert hasattr(self.box, 'vertex_data')
        assert hasattr(self.box, 'color_data')
        assert isinstance(self.box.box,
                          pyglet.graphics.vertexdomain.VertexList)

    def test_hide(self):
        self.box.show()
        self.box.hide()
        assert self.box.box is None


class TestMenu(TestCase):

    def setup(self):
        super(TestMenu, self).setup()
        self.x, self.y = 0, 0
        self.width, self.height = 350, 300
        self.text = ['Here Lies Text', 'the next text is hexed', 'inTEXTicated']
        self.functions = [lambda: None for i in range(3)]
        self.kwargs = {'box': True}
        self.create_menu()

    def create_menu(self):
        self.menu = gui.Menu(self.x, self.y, self.width, self.height, self.batch,
                             self.text, self.functions, **self.kwargs)

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
        assert self.menu.selection == -1

        assert isinstance(self.menu.box, gui.Box)
        assert all([isinstance(box, gui.Box) for box in self.menu.boxes])

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
            assert label.anchor_y == 'center'
            assert label.multiline == False
            assert label.batch == self.batch

    def test_hit_test(self):
        for box in self.menu.boxes:
            x1 = box.x
            y1 = box.y
            x2 = x1 + box.width
            y2 = y1 + box.height
            for x, y in (
                    ((x1 + x2 - 1) / 2, (y1 + y2 - 1) / 2),
                    (x1, y1), (x1, y2 - 1), (x2 - 1, y1), (x2 - 1, y2 - 1)):
                assert self.menu.hit_test(x, y, box), 'i=' + str(
                    self.menu.boxes.index(box))
            for x, y in (
                    (x1 + x2, y1 + y2), (x1, y2), (x2, y1), (x2, y2)):
                assert not self.menu.hit_test(x, y, box), 'i=' + str(
                    self.menu.boxes.index(box))

    def test_select_item(self):
        old_i = self.menu.selection
        self.menu.select_item(1)
        assert not isinstance(self.menu.boxes[old_i].box,
                              pyglet.graphics.vertexdomain.VertexList)

        new_i = self.menu.selection
        assert new_i == 1
        assert isinstance(self.menu.boxes[new_i].box,
                          pyglet.graphics.vertexdomain.VertexList)

    def test_select_next(self):
        self.menu.select_item(0)
        self.menu.select_next()
        assert self.menu.selection == 1
        self.menu.select_next()
        self.menu.select_next()
        assert self.menu.selection == 0

    def test_select_prev(self):
        self.menu.select_item(1)
        self.menu.select_prev()
        assert self.menu.selection == 0
        self.menu.select_prev()
        assert self.menu.selection == len(self.text) - 1

    def test_deselect(self):
        self.menu.select_item(1)
        self.menu.deselect()
        assert self.menu.selection == -1

    def test_on_mouse_motion(self):
        for box in self.menu.boxes:
            x = box.x
            y = box.y
            for dx, dy in permutations((-1, 0, 1), 2):
                self.menu.on_mouse_motion(x, y, dx, dy)
                assert self.menu.selection == self.menu.boxes.index(box), \
                    'x={}, y={}, dx={}, dy={}, s={}, i={}'.format(
                        x, y, dx, dy, self.menu.selection,
                        self.menu.boxes.index(box))
                self.menu.on_mouse_motion(x, y + box.height, dx, dy)
                assert self.menu.selection != self.menu.boxes.index(box), \
                    'x={}, y={}, dx={}, dy={}, s={}, i={}'.format(
                        x, y, dx, dy, self.menu.selection,
                        self.menu.boxes.index(box))
        self.menu.on_mouse_motion(
            self.menu.boxes[-1].x * 2, self.menu.boxes[-1].y * 2, dx, dy)
        assert self.menu.selection == -1

        self.window.push_handlers(self.menu)
        self.run_app()
