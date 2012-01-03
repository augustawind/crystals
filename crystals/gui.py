"""simple gui components"""
import pyglet

def draw_box(x, y, width, height, batch):
    """Draw a box into a batch"""
    x2 = x + width
    y2 = y + height
    return batch.add(4, pyglet.gl.GL_QUADS, None,
                     ('v2i', [x, y, x, y2, x2, y, x2, y2]))


class Menu(object):

    def __init__(self, x, y, width, height, batch, text, functions):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        self.text = text
        self.functions = functions
    
        self.box = draw_box(x, y, width, height, batch)
