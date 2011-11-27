"""interface.py"""
from pyglet.text.layout import TextLayout, IncrementalTextLayout
from pyglet.text.document import FormattedDocument, UnformattedDocument
from pyglet.window import key, mouse
from pyglet.graphics import OrderedGroup, Batch
from pyglet.gl import GL_LINES

INTERFACE_GROUP = OrderedGroup(99)

class MessageBox:

    def __init__(self, game_window):
        self.game_window = game_window

        self.message_str = '==> '
        self.document = UnformattedDocument(
            self.message_str + 'Welcome!')
        self.document.set_style(0, 0,
                dict(font_name='monospace', font_size=12,
                    color=(255, 255, 255, 255)))
        
        self.layout = IncrementalTextLayout(self.document,
            self.game_window.width, 96, multiline=True,
            group=INTERFACE_GROUP)
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

class PauseMenu:

    def __init__(self, game_window):
        self.game_window = game_window

        self.batch = Batch()

        self.blank_document = UnformattedDocument('EMPTY')
        self.main_document = UnformattedDocument(
            '(p) Party\n\n' +
            '(i) Inventory\n\n' +
            '(j) Journal\n\n' +
            '(s) Suspend\n\n')

        style = dict(font_name='monospace', font_size=16,
                    color=(255, 255, 255, 255))
        self.main_document.set_style(0, 0, style)
        self.blank_document.set_style(0, 0, style)

        margin = 10
        padding = 50

        self.panel_left = TextLayout(self.main_document,
            (game_window.width / 2) - (margin * 2),
            game_window.height - (margin * 2),
            multiline=True, batch=self.batch)
        self.panel_left.anchor_x = 'left'
        self.panel_left.anchor_y = 'top'
        self.panel_left.x = padding / 2
        self.panel_left.y = game_window.height - (padding / 2)

        self.panel_right = TextLayout(self.blank_document,
            (game_window.width / 2) - (margin * 2),
            game_window.height - (margin * 2),
            multiline=True, batch=self.batch)
        self.panel_right.anchor_x = 'left'
        self.panel_right.anchor_y = 'top'
        self.panel_right.x = (game_window.width / 2) + (padding / 2)
        self.panel_right.y = game_window.height - (padding / 2)

        self.border = self.batch.add_indexed(6, GL_LINES, None,
            [0, 2, 2, 5, 0, 3, 3, 5, 1, 4],
            ('v2i',
            (margin, margin,
            game_window.width / 2, margin,
            game_window.width - margin, margin,
            margin, game_window.height - margin,
            game_window.width / 2, game_window.height - margin,
            game_window.width - margin, game_window.height - margin)))

    def on_draw(self):
        self.game_window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.B:
            self.game_window.activate_world_mode()
    
    def activate(self):
        self.game_window.on_text_motion = lambda motion: None
        self.game_window.on_text = lambda text: None
        self.game_window.on_draw = self.on_draw
        self.game_window.on_key_press = self.on_key_press

class MainMenu:

    def __init__(self, game_window):
        self.game_window = game_window

        self.document = FormattedDocument(
            u'CRY\u00A7TAL\u00A7\n\n' +
            u'(n) new game\n' +
            u'(l) load game\n' +
            u'(q) quit')
        self.document.set_style(0, len(self.document.text),
                dict(font_name='monospace', color=(255, 255, 255, 255)))
        self.document.set_paragraph_style(0, 2, dict(font_size=36))
        self.document.set_paragraph_style(1, 4, dict(font_size=18))

        self.layout = TextLayout(self.document,
            game_window.width / 2, game_window.height, multiline=True)
        self.layout.content_valign = 'center'
        self.layout.x = (self.game_window.width // 2) - \
            (self.layout.width // 2)
        self.layout.y = (self.game_window.height // 2) - \
            (self.layout.height // 2)

    def on_draw(self):
        self.game_window.clear()
        self.layout.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in (key.Q, key.ESCAPE):
            self.game_window.quit()
        elif symbol == key.N:
            self.game_window.new_game()
        elif symbol == key.L:
            self.game_window.load_game()

    def activate(self):
        self.game_window.on_key_press = self.on_key_press
        self.game_window.on_draw = self.on_draw
