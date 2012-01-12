import pyglet
from pyglet.window import key

from crystals.loaders import WorldLoader
from crystals.gui import Menu

# Use the data/ and res/ directories in the test suite when debugging
if __debug__:
    from test.helpers import DATA_PATH, RES_PATH

class Game(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.win_width = 600
        self.win_height = 400
        self.window = pyglet.window.Window(self.win_width, self.win_height)
        self.window.clear()
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()

        self.main_menu = Menu(
            0, 0, self.win_width, self.win_height, self.batch,
            ['new game', 'quit'],
            [self.new_game, pyglet.app.exit],
            show_box=True, bold=True)
        self.world = None

    def run(self):
        self.window.push_handlers(self.main_menu)
        pyglet.app.run()

    def new_game(self):
        self.window.pop_handlers()
        self.window.clear()
        loader = WorldLoader(self.batch, DATA_PATH, RES_PATH)
        self.world = loader.load_room('TestRoom1')
