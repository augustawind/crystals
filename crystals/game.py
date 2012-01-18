"""top-level game logic"""
import os.path

import pyglet
from pyglet.window import key

from crystals.gui import Menu
from crystals.data import ImageDict
from crystals.data import WorldLoader
from crystals.data import RES_PATH
from crystals.entity import Entity
from crystals.world import World

# Use the resource directory in the test suite when debugging
if __debug__:
    from test.helpers import RES_PATH

class GameMode(object):
    """Abstract class for top-level game objects with event handlers."""

    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()

    def activate(self):
        """Push all event handlers onto the window."""
        self.window.push_handlers(self)

    def on_draw(self):
        """Clear the window and repaint the batch."""
        self.window.clear()
        self.batch.draw()


class MainMenu(GameMode, Menu):
    """Game mode that displays a menu. Greets the player."""

    def __init__(self, window, new_game):
        GameMode.__init__(self, window)
        Menu.__init__(
            self, 0, 0, window.width, window.height, self.batch,
            ['new game', 'quit'],
            [new_game, pyglet.app.exit],
            show_box=True, bold=True)


class WorldMode(GameMode):
    """Game mode where the player explores the game world."""

    def __init__(self, window, world, hero):
        GameMode.__init__(self, window)
        self.world = world
        self.hero = hero

    def activate(self):
        self.batch = self.world.focus.batch
        GameMode.activate(self)


class Game(object):
    """The main application object. Runs the game."""

    def __init__(self):
        self.win_width = 600
        self.win_height = 400
        self.window = pyglet.window.Window(self.win_width, self.win_height)
        self.window.clear()

        self.main_menu = MainMenu(self.window, self.new_game)
        self.world = None
        self.hero = None

    def run(self):
        """Run the game, activating the main menu."""
        self.main_menu.activate()
        pyglet.app.run()

    def new_game(self):
        """Initialize and start a new game in world mode."""
        self.window.pop_handlers()
        self.window.clear()

        loader = WorldLoader(RES_PATH)
        world = loader.load_world()

        images = ImageDict('character', os.path.join(RES_PATH, 'image'))
        hero = Entity('character', 'hero', False, images['human-peasant'])
        self.world = WorldMode(self.window, world, hero)
        self.world.activate()
