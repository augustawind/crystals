"""simple gui components"""
import pyglet

COLOR_WHITE = (255, 255, 255, 255)

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
        x2 = self.x + self.width
        y2 = self.y + self.height
        size = 5
        self.vertex_data = ('v2i', (self.x, self.y,
                                    self.x, y2,
                                    x2, y2,
                                    x2, self.y,
                                    self.x, self.y))
        self.color_data = ('c4B', self.color * size)
        self.box = self.batch.add(size, pyglet.gl.GL_LINE_STRIP, None,
                  self.vertex_data, self.color_data)

    def hide(self):
        self.box.delete()


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

        self.box = Box(self.x, self.y, self.width, self.height,
                            self.batch, color, box)

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
                         color, show=True))
            box_y += box_height 

            label_y += box_height
            self.labels.append(pyglet.text.Label(
                self.text[i], font_name, font_size, bold, italic, color,
                label_x, label_y, label_width, label_height,
                anchor_x='center', anchor_y='baseline',
                halign='center', multiline=False, batch=self.batch))
            self.labels[-1].content_valign = 'center'
