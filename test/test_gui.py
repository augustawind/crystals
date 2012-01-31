from itertools import permutations

from nose.tools import *
from pyglet.graphics.vertexdomain import VertexList
import pyglet

from test.util import *
from crystals import gui
from crystals.world import TILE_SIZE


class TestBox(object):

    def setup(self):
        self.batch = pyglet.graphics.Batch()
        self.args = (0, 0, 50, 50, self.batch, gui.COLOR_RED)
        self.box = gui.Box(*self.args)

    def TestInit_IfShowIsFalse_DontShowBox(self):
        assert not self.box.box

    def TestInit_IfShowIsTrue_ShowBox(self):
        self.args += (True,)
        self.box = gui.Box(*self.args) 
        assert isinstance(self.box.box, VertexList)

    def TestVisible_IfBoxEvalsFalse_ReturnFalse(self):
        assert not self.box.visible

    def TestVisible_IfBoxEvalsTrue_ReturnTrue(self):
        self.box.box = True
        assert self.box.visible

    def TestShow_IfBoxNotVisible_ShowBox(self):
        self.box.show()
        assert isinstance(self.box.box, VertexList)

    def TestHide_IfBoxIsVisible_HideBox(self):
        self.box.show()
        self.box.hide()
        assert not self.box.box

    def TestHide_IfBoxIsNotVisible_DoNothing(self):
        self.box.hide()
        assert not self.box.box


class TestMenu(PygletTestCase):

    def setup(self):
        PygletTestCase.setup(self)

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

    def TestInit_CheckSimpleAttrs(self):
        assert isinstance(self.menu, gui.Menu)
        assert self.menu.batch == self.batch
        assert self.menu.functions == self.functions
        assert self.menu.selection == -1
        assert isinstance(self.menu.box, gui.Box)

    def TestInit_AllBoxesInheritFromGuiBoxClass(self):
        for box in self.menu.boxes:
            assert isinstance(box, gui.Box)

    def TestInit_LabelAttrsHaveExpectedValues(self):
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

    def TestHitTest_WithinBounds_ReturnsTrue(self):
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

    def TestHitTest_OutOfBounds_ReturnsFalse(self):
        for box in self.menu.boxes:
            x1 = box.x
            y1 = box.y
            x2 = x1 + box.width
            y2 = y1 + box.height
            for x, y in (
                    (x1 + x2, y1 + y2), (x1, y2), (x2, y1), (x2, y2)):
                assert not self.menu.hit_test(x, y, box), 'i=' + str(
                    self.menu.boxes.index(box))

    def TestSelectItem_ValidInput_DeselectCurrentItem(self):
        old_i = self.menu.selection
        self.menu.select_item(1)
        assert not self.menu.boxes[old_i].box

    def TestSelectItem_ValidInput_SelectGivenItem(self):
        self.menu.select_item(1)
        new_i = self.menu.selection
        assert isinstance(self.menu.boxes[new_i].box,
                          pyglet.graphics.vertexdomain.VertexList)

    def TestSelectNext_ShortOfLastItem_SelectNextItem(self):
        self.menu.select_item(0)
        self.menu.select_next()
        assert self.menu.selection == 1

    def TestSelectNext_LastItemSurpassed_SelectFirstItem(self):
        self.menu.select_item(2)
        self.menu.select_next()
        assert self.menu.selection == 0

    def TestSelectPrev_ShortOfFirstItem_SelectPrevItem(self):
        self.menu.select_item(1)
        self.menu.select_prev()
        assert self.menu.selection == 0

    def TestSelectPrev_FirstItemSurpassed_SelectLastItem(self):
        self.menu.select_item(0)
        self.menu.select_prev()
        assert self.menu.selection == len(self.text) - 1

    def TestDeselect_ItemSelected_DeselectItem(self):
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
            self.menu.boxes[-1].width * 2, self.menu.boxes[-1].y * 2, dx, dy)
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


class TestTextFeed(PygletTestCase):

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

    def test_write(self):
        textfeed = gui.TextFeed(
            5, 5, self.window.width - 5, self.window.height - 5, self.batch,
            True)
        assert all(label.text == '' for label in textfeed.labels)

        text = 'Hello, world!!!'
        for i in range(len(textfeed.labels) - 1):
            textfeed.write(text)
            assert textfeed.labels[-(i + 1)].text == text
            assert all(label.text == '' for label in textfeed.labels[:-(i + 1)])

        textfeed.write(text)
        assert all(label.text == text for label in textfeed.labels)
        textfeed.write('Goodbye, cruel world...')
        assert textfeed.labels[0].text == 'Goodbye, cruel world...'
        assert all(label.text == text for label in textfeed.labels[1:])
