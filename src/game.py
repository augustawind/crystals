"""game.py"""
import pyglet
from pyglet.text.layout import TextLayout
from pyglet.text.document import FormattedDocument, UnformattedDocument
from pyglet.window import key, mouse

import data

class MainMenu:

    def __init__(self, game_window):
        self.game_window = game_window

        self.document = FormattedDocument(
            '<<< ??? >>>\n\n' +
            '(n) new game\n' +
            '(l) load game\n' +
            '(q) quit')
        self.document.set_style(0, len(self.document.text),
                dict(font_name='monospace', color=(255, 255, 255, 255)))
        self.document.set_paragraph_style(0, 2, dict(font_size=36))
        self.document.set_paragraph_style(1, 4, dict(font_size=18))

        self.layout = TextLayout(self.document, 200, 200, multiline=True)
        self.layout.x = (self.game_window.width // 2) - \
            (self.layout.width // 2)
        self.layout.y = (self.game_window.height // 2) - \
            (self.layout.height // 2)

    def on_draw(self):
        self.game_window.clear()
        self.draw()

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

    def draw(self):
        self.layout.draw()

class Game(pyglet.window.Window):
    """The main application class. Runs the game!"""

    def __init__(self):
        super(Game, self).__init__(640, 680, caption='<<< ??? >>>',
            resizable=False)

        # main menu
        self.main_menu = MainMenu(self)
        # world
        self.world = None
        # combat
        self.combat = None
        # hero
        self.hero = None

    def update_mode(self, mode):
        {'mainmenu': self.main_menu.activate,
            'world': self.activate_world_mode}[mode]()

    def new_game(self):
        self.world = data.load_world()

        self.update_mode('world')

    def load_game(self):
        pass

    def quit(self):
        pyglet.app.exit()

    def run(self):
        """Run the game."""
        self.update_mode('mainmenu')
        pyglet.app.run()

    def activate_world_mode(self):
        self.hero = self.world.get_hero()

        def on_draw():
            self.clear()
            self.world.draw()

        def on_key_press(symbol, modifiers):
            """World mode controls. User can move Hero to interact with other
            Entities in World, initiate Combat, and access the pause menu."""
            if symbol == key.H:
                self.world.step_entity(self.hero, -1, 0)
            elif symbol == key.J:
                self.world.step_entity(self.hero, 0, -1)
            elif symbol == key.K:
                self.world.step_entity(self.hero, 0, 1)
            elif symbol == key.L:
                self.world.step_entity(self.hero, 1, 0)

        self.on_draw = on_draw
        self.on_key_press = on_key_press

if __name__ == '__main__':
    game = Game()
    game.run()
