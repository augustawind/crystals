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

    def show(self):
        if self.box:
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
        if self.box:
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
        box_height = (self.height / len(text)) - (margin)

        label_width = box_width - (padding * 2)
        label_height = box_height - (padding * 2)
        label_x = (box_x + box_width) / 2
        label_y = box_y + padding - (label_height / 2)

        self.boxes = []
        self.labels = []
        for i in range(len(self.text)):
            self.boxes.append(
                Box(box_x, box_y, box_width, box_height, self.batch,
                         color, show=False))
            box_y += box_height 

            label_y += box_height
            self.labels.append(pyglet.text.Label(
                self.text[i], font_name, font_size, bold, italic, color,
                label_x, label_y, label_width, label_height,
                anchor_x='center', anchor_y='baseline',
                halign='center', multiline=False, batch=self.batch))
            self.labels[-1].content_valign = 'center'

    def select_item(self, i):
        if i == self.selection:
            return
        self.boxes[self.selection].hide()
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

