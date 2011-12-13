import pyglet.app

from pyguit import MenuButton, Menu, TextFeed

from crystals.world import VIEWPORT, TILE_SIZE
from crystals.data import ImageLoader, load_fonts

__all__ = ['MainMenu', 'PauseMenu', 'CombatMenu', 'MessageBox']

FONT_RUNESCAPE_UF = 'Runescape UF'
FONT_TERMINUS = 'Terminus'
DEFAULT_FONT = FONT_RUNESCAPE_UF

images = ImageLoader()
load_fonts()

class MainMenu(Menu):

    def __init__(self, window, batch=None):
        super(MainMenu, self).__init__(
            #window.width // 4, window.height // 4,
            10, 10,
            anchor_x='left', anchor_y='left')

        style = {'font_name': DEFAULT_FONT, 'font_size': 24,
                 'color': (255, 255, 255, 255)}
        padding = 10
        width = 140
        height = style['font_size'] + (padding * 2)
        
        self.bg = pyglet.graphics.OrderedGroup(0)
        self.fg = pyglet.graphics.OrderedGroup(1)

        self.add(MenuButton(0, 0, width, height, "QUIT", func=pyglet.app.exit,
                            style=style, padding=padding, group=self.fg))
        self.add(MenuButton(0, height, width, height, "LOAD GAME",
                            func=window.load_game, style=style,
                            padding=padding, group=self.fg))
        self.add(MenuButton(0, height * 2, width, height, "NEW GAME",
                            func=window.new_game, style=style,
                            padding=padding, group=self.fg))
        self.update()

        image = images['interface']['album-cover']
        image.width = window.width
        image.height = window.height
        self.sprite = pyglet.sprite.Sprite(
            image, batch=self.batch, group=self.bg)

    def activate(self, window):
        def on_draw():
            window.clear()
            self.draw()
        window.push_handlers(self, on_draw)
