"""simple gui components"""
import pyglet

COLOR_WHITE = (255, 255, 255, 255)
COLOR_RED = (255, 0, 0, 255)

ANCHOR_X = 'left'
ANCHOR_Y = 'bottom'

class Box(object):

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
        return self.box is not None

    def show(self):
        if self.visible:
            return
        x2 = self.x + self.width
        y2 = self.y + self.height
        size = 8
        self.vertex_data = ('v2i', (self.x, self.y, self.x, y2,
                                    self.x, self.y, x2, self.y,
                                    x2, self.y, x2, y2,
                                    self.x, y2, x2, y2))
        self.color_data = ('c4B', self.color * size)
        self.box = self.batch.add(size, pyglet.gl.GL_LINES, None,
                  self.vertex_data, self.color_data)

    def hide(self):
        if self.visible:
            self.box.delete()
            self.box = None


class Menu(object):

    def __init__(self, x, y, width, height, batch, text, functions,
                 box=False, margin=10, padding=10, 
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
                       color, box)

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
        if (box.x <= x < box.x + box.width and
                box.y <= y < box.y + box.height):
            return True
        return False

    def select_item(self, i):
        if i == self.selection:
            return
        self.deselect()
        if i != -1:
            self.boxes[i].show()
            self.selection = i
    
    def select_next(self):
        if self.selection < len(self.text) - 1:
            self.select_item(self.selection + 1)
        else:
            self.select_item(0)

    def select_prev(self):
        if self.selection > 0:
            self.select_item(self.selection - 1)
        else:
            self.select_item(len(self.text) - 1)

    def deselect(self):
        if self.boxes[self.selection].visible:
            self.boxes[self.selection].hide()
            self.selection = -1

    # event handlers ---------------------------------------------------
    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.boxes:
            if self.hit_test(x, y, box):
                self.select_item(self.boxes.index(box))
                return
        self.deselect()
