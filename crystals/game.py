"""top-level game logic"""
import os.path

import pyglet
from pyglet.window import key

from crystals import data
from crystals.data import RES_PATH
from crystals import gui
from crystals.entity import Entity
from crystals.world import World

if __debug__:
    # Use the resource path used in the test suite 
    from test.util import RES_PATH


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

        # Define possible user inputs and their effects.
        # Values are each a tuple of a callable followed optionally by 
        # arguments.
        self.inputdict = {
            key.MOTION_LEFT: (self.step_player, -1, 0),
            key.MOTION_RIGHT: (self.step_player, 1, 0),
            key.MOTION_DOWN: (self.step_player, 0, -1),
            key.MOTION_UP: (self.step_player, 0, 1),

            key.SPACE: (self.interact,),
        }

    def activate(self):
        """Activate world mode."""
        self.infobox.activate()
        GameMode.activate(self)

    def set_focus(self, room_name):
        """Set the room with name `room_name` as the focus."""
        self.world.set_focus(room_name)
        self.batch = self.world.focus.batch

    def step_player(self, xstep, ystep):
        """Step the player (`xstep`, `ystep`) tiles from her current
        position.

        If successful and the new position hosts a portal, portal
        the player.
        """
        success = self.world.step_entity(self.player, xstep, ystep)
        if not success:
            return

        x, y, z = self.world.focus.get_coords(self.player)
        portal = self.world.get_portal(x, y)
        if portal:
            self.portal_player(portal)

    def portal_player(self, portal):
        """Transfer the player to the portal's destination, then set
        that room as the focus.
        """
        self.world.portal_entity(self.player, portal)
        self.set_focus(portal.to_room.name)

    def interact(self):
        """If an interactable entity is in front of the player, make
        her interact with it. Else, do nothing."""

    def on_key_press(self, key, modifiers):
        """Process user input."""
        if key not in self.inputdict:
            return
        self.inputdict[key][0](*self.inputdict[key][1:])


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
