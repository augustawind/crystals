"""top-level game logic"""
import os.path

import pyglet
from pyglet.window import key

from crystals import data
from crystals.data import RES_PATH
from crystals import gui
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


class MainMenu(GameMode, gui.Menu):
    """Game mode that displays a menu. Greets the player."""

    def __init__(self, window, new_game):
        GameMode.__init__(self, window)
        gui.Menu.__init__(
            self, 0, 0, window.width, window.height, self.batch,
            ['new game', 'quit'],
            [new_game, pyglet.app.exit],
            show_box=True, bold=True)


class WorldMode(GameMode):
    """Game mode where the player explores the game world."""

    def __init__(self, window, world, player):
        GameMode.__init__(self, window)
        self.world = world
        self.player = player
        self.batch = self.world.focus.batch
        
        tf_margin = 10
        tf_x = tf_y = tf_margin
        tf_width = window.width - (tf_margin * 2)
        tf_height = 100
        self.infobox = gui.TextFeed(tf_x, tf_y, tf_width, tf_height,
                                     self.batch, show_box=True)
        self.infobox.write('Welcome...')
        self.infobox.write('Welcome...')
        self.infobox.write('Welcome...')
        self.infobox.write('Welcome...')
        self.infobox.write('Welcome...')
        self.infobox.write('Welcome...')

    def activate(self):
        self.infobox.activate()
        GameMode.activate(self)

    def set_focus(self, room_name):
        self.world.set_focus(room_name)
        self.batch = self.world.focus.batch

    def portal_player(self, portal):
        """Transfer the player to the portal's destination, then set
        that room as the focus.
        """
        self.world.portal_entity(self.player, portal)
        self.set_focus(portal.to_room.name)

    def on_text_motion(self, motion):
        xstep, ystep = {key.MOTION_LEFT: (-1, 0),
                        key.MOTION_RIGHT: (1, 0),
                        key.MOTION_DOWN: (0, -1),
                        key.MOTION_UP: (0, 1)}[motion]
        self.world.step_entity(self.player, xstep, ystep)

        x, y, z = self.world.focus.get_coords(self.player)
        portal = self.world.get_portal(x, y)
        if portal:
            self.portal_player(portal)


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
        pyglet.app.run()

    def new_game(self):
        """Initialize and start a new game in world mode."""
        self.window.pop_handlers()
        self.window.clear()

        world, player = data.load_setting(RES_PATH)
        self.world = WorldMode(self.window, world, player)
        self.world.activate()
