import pyglet

from gui import Menu

class Game(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.win_width = 600
        self.win_height = 400
        self.window = None
        self.main_menu = Menu(
            0, 0, self.win_width, self.win_height, self.batch,
            ['new game', 'quit'],
            [lambda: None, pyglet.app.exit],
            show_box=True, bold=True)

    def run(self):
        self.window = pyglet.window.Window(self.win_width, self.win_height)
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()

        self.window.push_handlers(self.main_menu)
        pyglet.app.run()
