"""game.py"""
import random
import logging
import sys

import pyglet
from pyglet.window import key, mouse

import data
import interface

class Game(pyglet.window.Window):
    """The main application class. Runs the game!"""

    def __init__(self):
        super(Game, self).__init__(640, 680, caption='CRYSTALS',
            resizable=False)

        self.main_menu = interface.MainMenu(self)
        self.message_box = interface.MessageBox(self)

        self.world = None
        self.combat = None
        self.hero = None

        # world mode variables ------------------------------------------------

        self.base_delay = 0.125
        self.wander_frequency = 0.05
        self.key_pressed = (None, None)

        # dict of argument tuples for calls to Interactable.interact,
        # indexed by str(Interactable)
        self.interact_args = {
            'TextInteractable': (self.message_box, )}

        # keyboard controls
        self.movement_keys = {
            'up': key.UP,
            'down': key.DOWN,
            'left': key.LEFT,
            'right': key.RIGHT}
        self.interact_key = key.SPACE

    # application logic
    # -------------------------------------------------------------------------

    def run(self):
        """Run the game."""
        self.update_mode('mainmenu')
        pyglet.app.run()

    def update_mode(self, mode):
        {'mainmenu': self.main_menu.activate,
            'world': self.activate_world_mode}[mode]()

    # main menu mode methods
    # -------------------------------------------------------------------------

    def new_game(self):
        world_loader = data.WorldLoader()
        self.world = world_loader.load_world()
        self.hero = self.world.get_hero()

        self.update_mode('world')

    def load_game(self):
        pass

    def quit(self):
        pyglet.app.exit()

    # world mode methods
    # -------------------------------------------------------------------------

    def activate_world_mode(self):
        def on_draw():
            self.clear()
            self.message_box.draw()
            self.world.draw()

        def on_key_press(symbol, modifiers):
            """World mode controls. User can move Hero to interact with other
            Entities in World, initiate Combat, and access the pause menu."""
            self.key_pressed = (symbol, modifiers)

        def on_key_release(symbol, modifiers):
            self.key_pressed = (None, None)

        self.on_draw = on_draw
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

        pyglet.clock.schedule_interval(self.update_characters, self.base_delay)

    def update_characters(self, dt):
        for character in self.world.get_characters():
            if character is self.hero:
                symbol, modifiers = self.key_pressed
                if symbol in self.movement_keys.values():
                    self.hero_move(symbol)
                elif symbol == self.interact_key:
                    self.hero_interact()
            else:
                self.npc_wander(character)

    # hero methods
    # -------------------------------------------------------------------------

    def hero_move(self, symbol):
        x = 0
        y = 0
        if symbol == self.movement_keys['left']:
            x = -1
        if symbol == self.movement_keys['down']:
            y = -1
        if symbol == self.movement_keys['up']:
            y = 1
        if symbol == self.movement_keys['right']:
            x = 1

        self.world.step_hero(x, y)
        self.hero.set_direction(x, y)

    def hero_interact(self):
        x_dir, y_dir = self.hero.get_direction()
        x, y = self.world.get_coords(self.hero)
        interactable = self.world.get_interactable(x + x_dir, y + y_dir)
        if interactable:
            args = self.interact_args[str(interactable)]
            interactable.interact(*args)

    # npc methods
    # -------------------------------------------------------------------------

    def _choose_wander_dir(self, axes, x_dirs, y_dirs):
        axis = axes[0]
        if axis == 'x':
            x_dir = x_dirs.pop()
            y_dir = 0
        else:
            x_dir = 0 
            y_dir = y_dirs.pop()
        if not x_dirs and 'x' in axes:
            axes.remove('x')
        elif not y_dirs and 'y' in axes:
            axes.remove('y')
        return x_dir, y_dir

    def npc_wander(self, character):
        if random.random() < self.wander_frequency:
            axes = sorted(['x', 'y'], key=lambda x: random.random())
            x_dirs = sorted([-1, 1], key=lambda x: random.random())
            y_dirs = sorted([-1, 1], key=lambda x: random.random())
            x_dir, y_dir = self._choose_wander_dir(axes, x_dirs, y_dirs)
            while not self.world.step_entity(character, x_dir, y_dir):
                x_dir, y_dir = self._choose_wander_dir(axes, x_dirs, y_dirs)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
        format='%(levelname)s:%(message)s')

    game = Game()
    game.run()
