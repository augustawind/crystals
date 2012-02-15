"""event handlers for all the different top-level game modes"""
import pyglet
from pyglet.window import key

from crystals import gui
from crystals.world import Entity


class GameMode(object):
    """Abstract class for top-level game objects with event handlers."""

    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()

    def __repr__(self):
        """For identification purposes."""
        return self.__class__.__name__

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


    def __init__(self, window, world, player, plot, plot_state):
        GameMode.__init__(self, window)
        self.world = world
        self.player = player
        self.plot = plot
        self.plot_state = plot_state
        self.plot.send(self)

        self.batch = pyglet.graphics.Batch()
        self.world.batch = self.batch
        self.world.set_focus()
        
        ib_padding = 10
        ib_x = ib_y = ib_padding
        ib_width = window.width - (ib_padding * 2)
        ib_height = 100
        ib_style = dict(font_size=10, line_spacing=20)
        self.infobox = gui.InfoBox(
            ib_x, ib_y, ib_width, ib_height, self.batch, show_box=True,
            style=ib_style)

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
            if entity and entity.action:
                entity.action(self, entity)


    def on_key_press(self, key, modifiers):
        """Process user input."""
        if key not in self.inputdict:
            return
        self.inputdict[key][0](*self.inputdict[key][1:])
