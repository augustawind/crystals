"""interface.py - game menus, menu input, and text"""
from abc import ABCMeta

import pyglet
from pyglet.text.layout import TextLayout, IncrementalTextLayout
from pyglet.text.document import FormattedDocument, UnformattedDocument
from pyglet.window import key, mouse
from pyglet.gl import GL_LINES

pyglet.font.add_file('data/font/runescape_uf.ttf')
pyglet.font.add_file('data/font/terminus.ttf')

FONT_RUNESCAPE_UF = 'Runescape UF'
FONT_TERMINUS = 'Terminus'
DEFAULT_FONT = FONT_RUNESCAPE_UF

class Menu(object):
    """When activated, displays a list of options with corresponding keyboard
    keys and handles corresponding key presses."""
    
    __metaclass__ = ABCMeta

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

    __metaclass__ = ABCMeta

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

    def __init__(self, game_window):
        super(MainMenu, self).__init__(game_window)

        self.options = {
            key.N: game_window.new_game,
            key.L: game_window.load_game,
            key.Q: game_window.quit}

        # content -------------------------------------------------------------
        self.document = FormattedDocument(
            u'CRY\u00A7TAL\u00A7\n\n' +
            u'(n) NEW GAME\n' +
            u'(l) LOAD GAME\n' +
            u'(q) QUIT')

        # style ---------------------------------------------------------------
        self.document.set_style(0, len(self.document.text),
                dict(font_name=DEFAULT_FONT, color=(255, 255, 255, 255)))
        self.document.set_style(3, 4, dict(font_name=FONT_TERMINUS))
        self.document.set_style(7, 8, dict(font_name=FONT_TERMINUS))
        self.document.set_paragraph_style(0, 2, dict(font_size=64))
        self.document.set_paragraph_style(1, 4, dict(font_size=24))

        # layout --------------------------------------------------------------
        self.layout = TextLayout(self.document,
            game_window.width / 2, game_window.height,
            multiline=True, batch=self.batch)
        self.layout.content_valign = 'center'
        self.layout.x = (self.game_window.width // 2) - \
            (self.layout.width // 2)
        self.layout.y = (self.game_window.height // 2) - \
            (self.layout.height // 2)

class PauseMenu(TwoPanelMenu):

    def __init__(self, game_window):
        super(PauseMenu, self).__init__(game_window,
            game_window.width, game_window.height, 10, 50)

        self.main_options = {
            key.ENTER: game_window.activate_world_mode,
            key.S: pyglet.app.exit()}
        self.options = self.main_options

        # content -------------------------------------------------------------
        self.main_document = UnformattedDocument(
            '(p) Party\n\n' +
            '(i) Inventory\n\n' +
            '(j) Journal\n\n' +
            '(s) Suspend\n\n')

        # style ---------------------------------------------------------------
        style = dict(font_name=DEFAULT_FONT, font_size=24,
                    color=(255, 255, 255, 255))
        self.main_document.set_style(0, 0, style)

        # layout --------------------------------------------------------------
        self.update_layout(self.main_document, self.blank_document)

class CombatMenu(TwoPanelMenu):

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

class MessageBox:

    def __init__(self, game_window):
        self.game_window = game_window

        self.message_str = '>>> '
        self.document = UnformattedDocument(
            self.message_str + 'Welcome!')
        self.document.set_style(0, 0,
                dict(font_name=DEFAULT_FONT, font_size=12,
                    color=(255, 255, 255, 255)))
        
        self.layout = IncrementalTextLayout(self.document,
            self.game_window.width, 96, multiline=True)
        self.layout.x = 0
        self.layout.y = 0

    def get_width(self):
        return self.layout.width

    def get_height(self):
        return self.layout.height

    def print_message(self, text):
        self.document.insert_text(len(self.document.text), 
            '\\\n' + self.message_str + text)
        self.layout.ensure_line_visible(-1)

    def draw(self):
        self.layout.draw()
