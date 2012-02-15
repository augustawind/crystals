"""top-level game logic"""
import os.path

import pyglet
from pyglet.window import key

from crystals import gui
from crystals import loader
from crystals.api.plot import GameOver
from crystals.engine import *

RES_PATH = 'res' # default path to variable game resources
WORLD_PATH = RES_PATH + '/world' # default path to variable world scripts
PLOT_PATH = RES_PATH + '/plot' # default path to variable plot scripts
IMG_PATH = RES_PATH + '/img' # default path to variable game images

if __debug__:
    from test.util import WORLD_PATH, PLOT_PATH, IMG_PATH


class Game(object):
    """The main application object. Runs the game."""

    def __init__(self):
        window_width = 400
        window_height = 400
        self.window = pyglet.window.Window(window_width, window_height)
        self.window.clear()

        self.main_menu = MainMenu(self.window, self.new_game)
        self.world = None
        self.player = None

    def run(self):
        """Run the game, activating the main menu."""
        self.main_menu.activate()

        try:
            pyglet.app.run()
        except GameOver:
            print 'Game over: all plot conditions were met'
            pyglet.app.exit()

    def new_game(self):
        """Initialize and start a new game in world mode."""
        self.window.pop_handlers()
        self.window.clear()

        world, player = loader.load_world(WORLD_PATH, IMG_PATH)
        plot, pstate = loader.load_plot(PLOT_PATH)
        self.wmode = WorldMode(self.window, world, player, plot, pstate)
        self.wmode.activate()
