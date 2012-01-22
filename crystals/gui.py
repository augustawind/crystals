"""simple gui components"""
import pyglet
from pyglet.window import mouse

COLOR_WHITE = (255, 255, 255, 255)
COLOR_RED = (255, 0, 0, 255)

class Box(object):
    """An empty rectangle."""

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
    """A menu of vertically stacked text buttons.

    When a button is clicked, its corresponding function is called.
    """

    def __init__(self, x, y, width, height, batch, text, functions,
                 show_box=False, margin=10, padding=10, 
                 font_name='monospace', font_size=16, bold=False,
                 italic=False, color=COLOR_WHITE):
        self.batch = batch
        self.functions = functions
        self.selection = -1

        self.box = Box(x, y, height, batch, color, show_box)

        # Create menu items -------------------------------------------
        # Each item is represented by a Box and a Label ---------------
        box_x = x + margin
        box_y = y + margin
        box_width = width - (margin * 2)
        box_height = (height / len(text)) - (margin * 2)
        y_step = box_height + (margin * 2)
        box_ycoords = reversed(range(box_y, height, y_step))

        label_width = box_width - (padding * 2)
        label_height = box_height - (padding * 2)
        label_x = (box_x + box_width) / 2
        label_y = (box_y + box_height) / 2
        label_ycoords = reversed(range(label_y, height, y_step))

        self.boxes = []
        self.labels = []
        for i, box_y, label_y in zip(
                range(len(text)), box_ycoords, label_ycoords):
            self.boxes.append(
                Box(box_x, box_y, box_width, box_height, batch, color,
                    show=False))

            self.labels.append(pyglet.text.Label(
                text[i], font_name, font_size, bold, italic, color,
                label_x, label_y, label_width, label_height,
                anchor_x='center', anchor_y='center',
                halign='center', multiline=False, batch=batch))
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
        if self.selection < len(self.labels) - 1:
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
            self.select_item(len(self.labels) - 1)

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


class TextFeed(object):
    """A box that can output text."""

    def __init__(self, x, y, width, height, batch, show_box=False,
                 margin=10, line_height=24, font_name='monospace',
                 font_size=16, bold=False, italic=False, color=COLOR_WHITE):
        self.batch = batch

        self.box = Box(x, y, width, height, batch, color, show_box)

        # Create a label for each line in the textfeed -----------------
        label_x = x + margin
        label_width = width - (margin * 2)
        label_height = max(font_size, line_height)
        margin += ((height - margin) % label_height) / 2
        y1 = y + margin
        y2 = y1 + height - (margin * 2)

        self.labels = []
        for label_y in range(y1, y2, label_height):
            self.labels.append(pyglet.text.Label(
                '', font_name, font_size, bold, italic, color,
                label_x, label_y, label_width, label_height,
                halign='center', multiline=False, batch=self.batch))
            self.labels[-1].content_valign = 'center'

    def activate(self):
        """Prepare for rendering."""
        for label in self.labels:
            label.batch = self.batch
        self.box.batch = self.batch

    def update(self, text):
        """Add some text, scrolling up if the the feed is full."""
        updated = False
        for label in reversed(self.labels):
            if not label.text:
                label.text = text
                updated = True
                break
        if updated:
            return

        # Move all text up a label, discarding the top text and assigning 
        # `text` to the bottom label
        for i in reversed(range(1, len(self.labels))):
            self.labels[i].text = self.labels[i - 1].text
        self.labels[0].text = text

