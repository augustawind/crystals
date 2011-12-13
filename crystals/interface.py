"""predefined menus and other interface components"""
import pyglet

from crystals.world import VIEWPORT, TILE_SIZE
from crystals.data import ImageLoader, load_fonts
from guilet.menu import *
from guilet.text import TextFeed
from guilet import color

__all__ = ['MainMenu', 'PauseMenu', 'CombatMenu', 'MessageBox']

FONT_RUNESCAPE_UF = 'Runescape UF'
FONT_TERMINUS = 'Terminus'
DEFAULT_FONT = FONT_RUNESCAPE_UF

images = ImageLoader()
load_fonts()

class MainMenu(Menu):

    def __init__(self, window):
        super(MainMenu, self).__init__(
            0, 0, window.width, window.height, pyglet.graphics.Batch(),
            window)
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        # add background image
        image = images['interface']['album-cover']
        image.width = window.width
        image.height = window.height
        self.sprite = pyglet.sprite.Sprite(image, 0, 0, batch=self.batch,
                                           group=self.background)
        
        # add menu items
        trigger_args = (pyglet.app.exit, window.load_game, window.new_game)
        text = ("QUIT", "LOAD GAME", "NEW GAME")
        text_args = {'font_name': DEFAULT_FONT, 'font_size': 24,
                          'color': color.WHITE}
        padding = 10
        width = 140
        height = text_args['font_size'] + (padding * 2)
        for i in range(len(text)):
            self.add(MenuItem(0, i * height, width, height,
                              self.batch, trigger_args[i], text=text[i],
                              text_args=text_args, group=self.foreground))


class PauseMenu(Menu):

    def __init__(self, window):
        super(PauseMenu, self).__init__(
            10, 10, window.width - 20, window.height - 20, 
            pyglet.graphics.Batch(), window, show_border=True)
        self.parent = MenuItem(0, 0, 0, 0, self.batch,
                               window.activate_world_mode)

        # add menu items
        trigger_args = (self.PartyMenu(window), self.InventoryMenu(window),
                         self.JournalMenu(window), pyglet.app.exit)
        text = ("PARTY", "INVENTORY", "JOURNAL", "SUSPEND")
        text_args = {'font_name': DEFAULT_FONT, 'font_size': 24,
                          'color': color.WHITE}
        padding = 10
        width = 140
        height = text_args['font_size'] + (padding * 2)
        for i in range(len(text)):
            x = 10
            y = self.height - ((i + 1) * height) - 10
            if isinstance(trigger_args[i], Menu):
                item_class = MenuBranch
            else:
                item_class = MenuItem
            self.add(item_class(
                x, y, width, height, self.batch, trigger_args[i],
                text=text[i], text_args=text_args))

    class PartyMenu(Menu):

        def __init__(self, window):pass

    class InventoryMenu(Menu):

        def __init__(self, window):pass

    class JournalMenu(Menu):

        def __init__(self, window):pass


