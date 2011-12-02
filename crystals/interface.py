"""menus and text"""
import abc

import pyglet
from pyglet.text.layout import TextLayout, IncrementalTextLayout
from pyglet.text.document import FormattedDocument, UnformattedDocument
from pyglet.window import key, mouse
from pyglet.gl import GL_LINES

from world import VIEWPORT, TILE_SIZE
from data import ImageLoader

FONT_RUNESCAPE_UF = 'Runescape UF'
FONT_TERMINUS = 'Terminus'
DEFAULT_FONT = FONT_RUNESCAPE_UF

images = ImageLoader()

class Menu(object):
    """When activated, displays a list of options with corresponding keyboard
    keys and handles corresponding key presses."""
    
    __metaclass__ = abc.ABCMeta

    def __init__(self, game_window):
        self.game_window = game_window
        self.batch = pyglet.graphics.Batch()

        self.options = {}

    def on_draw(self):
        self.game_window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.options.keys():
            self.options[symbol]()

    def activate(self):
        self.game_window.on_text_motion = lambda motion: None
        self.game_window.on_draw = self.on_draw
        self.game_window.on_key_press = self.on_key_press

class TwoPanelMenu(Menu):
    """A Menu with two vertical panels. Submenus appear on the right panel, and
    the content on each panel slides to the left when a submenu is accessed
    from a submenu."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, game_window, width, height, margin, padding):
        super(TwoPanelMenu, self).__init__(game_window)

        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding

        self.blank_document = UnformattedDocument('')

        # layout --------------------------------------------------------------
        self.panel_left = TextLayout(self.blank_document,
            (self.width / 2) - (self.margin * 2),
            self.height - (self.margin * 2),
            multiline=True, batch=self.batch)
        self.panel_left.anchor_x = 'left'
        self.panel_left.anchor_y = 'top'
        self.panel_left.x = self.padding / 2
        self.panel_left.y = self.height - (self.padding / 2)

        self.panel_right = TextLayout(self.blank_document,
            (self.width / 2) - (self.margin * 2),
            self.height - (self.margin * 2),
            multiline=True, batch=self.batch)
        self.panel_right.anchor_x = 'left'
        self.panel_right.anchor_y = 'top'
        self.panel_right.x = (self.width / 2) + (self.padding / 2)
        self.panel_right.y = self.height - (self.padding / 2)

        # primitives ----------------------------------------------------------
        self.border = self.batch.add_indexed(6, GL_LINES, None,
            [0, 2, 2, 5, 0, 3, 3, 5, 1, 4],
            ('v2i',
            (margin, margin,
            width / 2, margin,
            width - margin, margin,
            margin, height - margin,
            width / 2, height - margin,
            width - margin, height - margin)))

    def update_layout(self, document_left, document_right):
        self.panel_left.document = document_left
        self.panel_right.document = document_right

class MainMenu(Menu):
    """The menu that first greets the user when she runs the game."""

    def __init__(self, game_window):
        super(MainMenu, self).__init__(game_window)

        self.groups = [pyglet.graphics.OrderedGroup(0),
            pyglet.graphics.OrderedGroup(1)] 

        self.options = {
            key.N: game_window.new_game,
            key.L: game_window.load_game,
            key.Q: game_window.quit}

        # content -------------------------------------------------------------
        self.document = FormattedDocument(
            u'(N) NEW GAME\n' +
            u'(L) LOAD GAME\n' +
            u'(Q) QUIT')

        # style ---------------------------------------------------------------
        self.document.set_style(0, len(self.document.text),
                dict(font_name=DEFAULT_FONT, font_size=24,
                    color=(255, 255, 255, 255)))

        # layout --------------------------------------------------------------
        self.layout = TextLayout(self.document, width=game_window.width,
            multiline=True, batch=self.batch, group=self.groups[1])
        self.layout.content_valign = 'center'
        self.layout.x = 16
        self.layout.y = 16

        # background image ----------------------------------------------------
        image = images['interface']['album-cover']
        image.width = game_window.width
        image.height = game_window.height
        self.bg_image = pyglet.sprite.Sprite(image,
            batch=self.batch, group=self.groups[0])

class PauseMenu(TwoPanelMenu):
    """A menu that can be accessed in world mode to view relevant in-game
    information, make certain changes to characters and items, and quit the
    game."""

    def __init__(self, game_window):
        super(PauseMenu, self).__init__(game_window,
            game_window.width, game_window.height, 10, 50)

        self.main_options = {
            key.ENTER: game_window.activate_world_mode,
            key.S: pyglet.app.exit()}
        self.options = self.main_options

        # content -------------------------------------------------------------
        self.main_document = UnformattedDocument(
            '(P) Party\n\n' +
            '(I) Inventory\n\n' +
            '(J) Journal\n\n' +
            '(S) Suspend\n\n')

        # style ---------------------------------------------------------------
        style = dict(font_name=DEFAULT_FONT, font_size=24,
                    color=(255, 255, 255, 255))
        self.main_document.set_style(0, 0, style)

        # layout --------------------------------------------------------------
        self.update_layout(self.main_document, self.blank_document)

class CombatMenu(TwoPanelMenu):
    """The menu that is displayed in combat, allowing the player to make
    decisions about what her team will do."""

    def __init__(self, game_window):
        super(CombatMenu, self).__init__(game_window,
            game_window.width, 96, 5, 25)

        self.main_options = {
            key.M: self.select_move,
            key.A: self.select_attack,
            key.C: self.select_cast,
            key.U: self.select_use,
            key.P: self.select_crystal}
        
        self.options = self.main_options

        # content -------------------------------------------------------------
        self.main_document = UnformattedDocument(
            '(m) Move\n' +
            '(a) Attack\n' +
            '(c) Cast\n' +
            '(u) Use\n' +
            '(p) Crystal\n')

        # style ---------------------------------------------------------------
        style = dict(font_name=DEFAULT_FONT, font_size=12,
                    color=(255, 255, 255, 255))
        self.main_document.set_style(0, 0, style)

        # layout --------------------------------------------------------------
        self.update_layout(self.main_document, self.blank_document)

    def get_player_action(self):
        return self.player_action

    def select_move(self):
        self.player_action = 'move'

    def select_attack(self):
        self.player_action = 'attack'

    def select_cast(self):
        #self.player_action = 'cast'
        raise NotImplementedError('Casting spells has not been implemented')

    def select_use(self):
        #self.player_action = 'use'
        raise NotImplementedError('Using items has not been implemented')

    def select_crystal(self):
        #self.player_action = 'crystal'
        raise NotImplementedError('Evoking crystals has not been implemented')

class WorldFrame:

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        # primitives ----------------------------------------------------------
        x1 = VIEWPORT['x1'] * TILE_SIZE
        y1 = VIEWPORT['y1'] * TILE_SIZE
        x2 = VIEWPORT['x2'] * TILE_SIZE
        y2 = VIEWPORT['y2'] * TILE_SIZE
        self.border = self.batch.add_indexed(4, GL_LINES, None,
            [0, 1, 0, 2, 1, 2, 1, 3],
            ('v2i', (x1, y1,
                     x1, y2,
                     x2, y1,
                     x2, y2)))

    def draw(self):
        self.batch.draw()

class MessageBox:
    """Displays messages from the world in world mode. All textual information
    that is given to the player in world mode is done so through MessageBox."""

    def __init__(self, game_window):
        self.game_window = game_window

        self.batch = pyglet.graphics.Batch()

        margin = 8
        padding = 16

        # content -------------------------------------------------------------
        self.message_str = '>>> '
        self.document = FormattedDocument(
            self.message_str + 'Welcome!')

        # style ---------------------------------------------------------------
        self.style = dict(font_name=DEFAULT_FONT, font_size=12,
            color=(255, 255, 255, 255))
        self.document.set_paragraph_style(0, 1, self.style)
        
        # layout --------------------------------------------------------------
        width = ((VIEWPORT['x2'] - VIEWPORT['x1']) * TILE_SIZE) - (padding * 2)
        height = 96 - (padding * 2)
        self.layout = IncrementalTextLayout(self.document,
            width, height, multiline=True, batch=self.batch)
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'
        self.layout.x = padding
        self.layout.y = padding

    @property
    def width(self):
        return self.layout.width

    @property
    def height(self):
        return self.layout.height

    def print_message(self, text):
        doc_len = len(self.document.text)
        # document only registers newlines if there are two
        self.document.insert_text(doc_len, 
            '\n\n' + self.message_str + text)
        # delete the extra newline
        self.document.delete_text(doc_len, doc_len + 1)
        self.layout.ensure_line_visible(-1)

    def draw(self):
        self.batch.draw()
