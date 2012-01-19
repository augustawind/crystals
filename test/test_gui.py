from itertools import permutations

from nose.tools import *
from pyglet.graphics.vertexdomain import VertexList
import pyglet

from test.helpers import *
from crystals import gui
from crystals.world import TILE_SIZE

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
        assert (self.box.box is None or isinstance(self.box.box, VertexList))

    def test_visible(self):
        assert not self.box.visible
        self.box.show()
        assert self.box.visible

    def test_show(self):
        self.box.show()
        assert isinstance(self.box.box, VertexList)

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
        self.kwargs = {'show_box': True}

        # menu functions set self.test_number to 1, 2, and 3 respectively
        self.test_number = None
        def f0(): self.test_number = 0
        def f1(): self.test_number = 1
        def f2(): self.test_number = 2
        self.functions = (f0, f1, f2)

        self.menu = gui.Menu(
            self.x, self.y, self.width, self.height, self.batch,
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
        assert all(isinstance(box, gui.Box) for box in self.menu.boxes)

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

    def get_box_data(self):
        """Convenience function for test_on_mouse_motion and
           test_on_mouse_release."""
        return [(box, box.x, box.y) for box in self.menu.boxes]

    def test_on_mouse_motion(self):
        for box, x, y in self.get_box_data():
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

    def test_on_mouse_release(self):
        self.menu.select_item(-1)
        n = self.menu.on_mouse_release(0, 0, 1, 0)
        assert n == None
        for i in range(3):
            self.menu.select_item(i)
            self.test_number = None
            self.menu.on_mouse_release(0, 0, 1, 0)  # see self.functions
            assert self.test_number == i
            for mouse_button in (2, 4):
                self.test_number = None
                n = self.menu.on_mouse_release(0, 0, mouse_button, 0)
                assert self.test_number == None 


class TestTextFeed(TestCase):

    def test_labels(self):
        textfeed = gui.TextFeed(0, 0, self.window.width, self.window.height,
                                self.batch)
        assert len(textfeed.labels) == len(
            range(0, self.window.height, TILE_SIZE)) - 1

    def test_activate(self):
        textfeed = gui.TextFeed(0, 0, self.window.width, self.window.height,
                                pyglet.graphics.Batch())
        assert all(label.batch is not self.batch for label in textfeed.labels)
        assert textfeed.box.batch is not self.batch
        textfeed.batch = self.batch
        textfeed.activate()
        assert all(label.batch is self.batch for label in textfeed.labels)
        assert textfeed.box.batch is self.batch

    def test_update(self):
        textfeed = gui.TextFeed(
            5, 5, self.window.width - 5, self.window.height - 5, self.batch,
            True)
        assert all(label.text == '' for label in textfeed.labels)

        text = 'Hello, world!!!'
        for i in range(len(textfeed.labels) - 1):
            textfeed.update(text)
            assert textfeed.labels[-(i + 1)].text == text
            assert all(label.text == '' for label in textfeed.labels[:-(i + 1)])

        textfeed.update(text)
        assert all(label.text == text for label in textfeed.labels)
        textfeed.update('Goodbye, cruel world...')
        assert textfeed.labels[0].text == 'Goodbye, cruel world...'
        assert all(label.text == text for label in textfeed.labels[1:])
