"""simple gui components"""
import pyglet
from pyglet.window import mouse

COLOR_WHITE = (255, 255, 255, 255)
COLOR_RED = (255, 0, 0, 255)

class Box(object):
    """A rectangle that serves as a line border."""

    def __init__(self, x, y, width, height, batch, color=COLOR_WHITE,
                 show=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        self.color = color

        self.box = None
        if show:
            self.show()

    @property
    def visible(self):
        """Return True if the box is visible."""
        return self.box is not None

    def show(self):
        """Show the box. If it's already visible, do nothing."""
        if self.visible:
            return
        x2 = self.x + self.width
        y2 = self.y + self.height
        size = 8
        vertex_data = ('v2i', (self.x, self.y, self.x, y2,
                                    self.x, self.y, x2, self.y,
                                    x2, self.y, x2, y2,
                                    self.x, y2, x2, y2))
        color_data = ('c4B', self.color * size)
        self.box = self.batch.add(size, pyglet.gl.GL_LINES, None,
                  vertex_data, color_data)

    def hide(self):
        """Hide the box. If it's already invisible, do nothing."""
        if self.visible:
            self.box.delete()
            self.box = None


class Menu(object):
    """A menu of clickable/selectable text buttons that execute functions."""

    def __init__(self, x, y, width, height, batch, text, functions,
                 show_box=False, margin=10, padding=10, 
                 font_name='monospace', font_size=16, bold=False,
                 italic=False, color=COLOR_WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        self.text = text
        self.functions = functions
        self.selection = -1

        self.box = Box(self.x, self.y, self.width, self.height, self.batch,
                       color, show_box)

        # Create menu items -------------------------------------------
        # Each item is represented by a Box and a Label ---------------
        box_x = self.x + margin
        box_y = self.y + margin
        box_width = self.width - (margin * 2)
        box_height = (self.height / len(text)) - (margin * 2)

        label_width = box_width - (padding * 2)
        label_height = box_height - (padding * 2)
        label_x = (box_x + box_width) / 2
        label_y = box_y - label_height

        self.boxes = []
        self.labels = []
        for i in range(len(self.text)):
            self.boxes.append(
                Box(box_x, box_y, box_width, box_height, self.batch,
                         color, show=False))

            step = box_height + (margin * 2)
            box_y += step
            label_y += step

            self.labels.append(pyglet.text.Label(
                self.text[i], font_name, font_size, bold, italic, color,
                label_x, label_y, label_width, label_height,
                anchor_x='center', anchor_y='center',
                halign='center', multiline=False, batch=self.batch))
            self.labels[-1].content_valign = 'center'

    def hit_test(self, x, y, box):
        """Return True if (x, y) is within the bounds of box, else False."""
        if (box.x <= x < box.x + box.width and
                box.y <= y < box.y + box.height):
            return True
        return False

    def select_item(self, i):
        """Deselect the currently selected menu item, then select the
        menu item at index i, displaying its border.
        """
        if i == self.selection:
            return
        self.deselect()
        if i != -1:
            self.boxes[i].show()
            self.selection = i
    
    def select_next(self):
        """Select the next menu item in sequence.
        
        If the next index exceeds the highest item index, use the
        lowest index in the sequence.
        """
        if self.selection < len(self.text) - 1:
            self.select_item(self.selection + 1)
        else:
            self.select_item(0)

    def select_prev(self):
        """Select the previous menu item in sequence.

        If the previous index is below item index zero, use the
        highest index in the sequence.
        """
        if self.selection > 0:
            self.select_item(self.selection - 1)
        else:
            self.select_item(len(self.text) - 1)

    def deselect(self):
        """Deselect the current menu item if it is currently selected,
        else do nothing.
        """
        if self.selection != -1 and self.boxes[self.selection].visible:
            self.boxes[self.selection].hide()
            self.selection = -1

    # event handlers ---------------------------------------------------
    def on_mouse_motion(self, x, y, dx, dy):
        """Deselect the current menu item. Then, if the mouse is
        positioned within the bounds of a menu item's box, select that
        item.
        """
        self.deselect()
        for box in self.boxes:
            if self.hit_test(x, y, box):
                self.select_item(self.boxes.index(box))
                break 

    def on_mouse_release(self, x, y, button, modifiers):
        """On a left mouse release, if a button is currently selected,
        execute that button's corresponding function.
        """
        if self.selection != -1 and button == mouse.LEFT:
            self.functions[self.selection]()
