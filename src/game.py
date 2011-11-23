"""game.py"""
import random

import pyglet
from pyglet.window import key, mouse

import data
import interface

class Game(pyglet.window.Window):
    """The main application class. Runs the game!"""

    def __init__(self):
        super(Game, self).__init__(640, 680, caption='CRYSTALS',
            resizable=False)

        # main menu
        self.main_menu = interface.MainMenu(self)
        # world
        self.world = None
        # combat
        self.combat = None
        # hero
        self.hero = None

        # base clock delay
        self.base_delay = 0.5

        # added clock delays
        self.wander_delay = 0.5

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

    def schedule_interval(self, function, delay):
        pyglet.clock.schedule_interval(self.update_characters,
            self.base_delay + delay)

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
            elif symbol == key.Y:
                self.world.step_entity(self.hero, -1, 1)
            elif symbol == key.U:
                self.world.step_entity(self.hero, 1, 1)
            elif symbol == key.B:
                self.world.step_entity(self.hero, -1, -1)
            elif symbol == key.N:
                self.world.step_entity(self.hero, 1, -1)

        self.on_draw = on_draw
        self.on_key_press = on_key_press

        self.schedule_interval(self.update_characters, self.wander_delay)

    def _choose_wander_dir(self, axes, x_dirs, y_dirs):
        axis = axes[0]
        if axis == 'x':
            x_dir = x_dirs.pop()
            y_dir = 0
        else:
            x_dir = 0 
            y_dir = y_dirs.pop()
        if not x_dirs:
            axes.remove('x')
        elif not y_dirs:
            axes.remove('y')
        return x_dir, y_dir

    def update_characters(self, dt):
        for character in self.world.get_characters():
            if character is self.hero:
                continue

            axes = sorted(['x', 'y'], key=lambda x: random.random())
            x_dirs = sorted([-1, 1], key=lambda x: random.random())
            y_dirs = sorted([-1, 1], key=lambda x: random.random())
            x_dir, y_dir = self._choose_wander_dir(axes, x_dirs, y_dirs)
            while not self.world.step_entity(character, x_dir, y_dir):
                x_dir, y_dir = self._choose_wander_dir(axes, x_dirs, y_dirs)

if __name__ == '__main__':
    game = Game()
    game.run()
