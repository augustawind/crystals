"""top-level game logic"""
import os.path

import pyglet
from pyglet.window import key

from crystals import gui
from crystals import resource
from crystals.world import World, Entity

RES_PATH = 'res' # default path to variable game resources
WORLD_PATH = RES_PATH + '/world' # default path to variable world scripts
PLOT_PATH = RES_PATH + '/plot' # default path to variable plot scripts
IMG_PATH = RES_PATH + '/img' # default path to variable game images

if __debug__:
    from test.util import WORLD_PATH, PLOT_PATH, IMG_PATH


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

    def __init__(self, window, world, player, plot):
        GameMode.__init__(self, window)
        self.world = world
        self.player = player
        self.plot = plot
        self.batch = pyglet.graphics.Batch()
        plot.app = self

        self.world.batch = self.batch
        self.world.set_focus()
        
        tf_padding = 10
        tf_x = tf_y = tf_padding
        tf_width = window.width - (tf_padding * 2)
        tf_height = 100
        tf_style = dict(
            wrap=True, font_size=10, line_spacing=20, color=gui.COLOR_WHITE,
            font_name='monospace')
        self.infobox = gui.TextFeed(
            tf_x, tf_y, tf_width, tf_height, self.batch, show_box=True,
            style=tf_style)

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

        # Define arguments for the execute method of each Action subclass.
        self.action_args = {
            'Alert': (self.infobox,),
            'Talk': (self.infobox,),
            'UpdatePlot': (self.plot,),
        }

    def step_player(self, xstep, ystep):
        """Step the player (`xstep`, `ystep`) tiles from her current
        position.

        If successful and the new position hosts a portal, portal
        the player.
        """
        success = self.world.step_entity(self.player, xstep, ystep)
        if not success:
            return

        from_room = self.world.focus.name
        x, y, z = self.world.focus.get_coords(self.player)
        if self.world.portals_xy2dest[from_room].get((x, y)):
            self.portal_player(x, y)

    def portal_player(self, x, y):
        """Transfer the player to the destination of the portal at
        (x, y), then set that room as the focus.
        """
        self.world.portal_entity(self.player, x, y)
        from_room = self.world.focus.name
        dest = self.world.portals_xy2dest[from_room][(x, y)]
        self.world.set_focus(dest)

    def interact(self):
        """If an interactable entity is in front of the player, make
        her interact with it. Else, do nothing.
        """
        x, y, z = self.world.focus.get_coords(self.player)
        x += self.player.facing[0]
        y += self.player.facing[1]
        for entity in self.world.focus[y][x]:
            if entity:
                for action in entity.actions:
                    args = self.action_args[type(action).__name__]
                    action(entity, *args)

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

        world, player = resource.load_world(WORLD_PATH, IMG_PATH)
        plot = resource.load_plot(PLOT_PATH)
        self.wmode = WorldMode(self.window, world, player, plot)
        self.wmode.activate()
