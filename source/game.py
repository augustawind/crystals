"""game.py - top-level application logic"""

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
        self.pause_menu = interface.PauseMenu(self)
        self.message_box = interface.MessageBox(self)

        self.world = None
        self.combat = None
        self.hero = None

        # application variables -----------------------------------------------
        self.base_delay = 0.1
        self.wander_frequency = 0.2
        self.queued_input = None

        # dict of argument tuples for calls to Interactable.interact,
        # indexed by str(Interactable)
        self.interact_args = {
            'TextInteractable': (self.message_box, )}

        # keyboard controls
        self.movement_keys = {
            'up': key.MOTION_UP,
            'down': key.MOTION_DOWN,
            'left': key.MOTION_LEFT,
            'right': key.MOTION_RIGHT}
        self.interact_key = ' '
        self.pause_key = key.ENTER

    def run(self):
        """Run the game."""
        self.main_menu.activate()
        pyglet.app.run()

    # main menu methods
    # -------------------------------------------------------------------------

    def new_game(self):
        world_loader = data.WorldLoader()
        self.world = world_loader.load_world()
        self.hero = self.world.hero

        self.activate_world_mode()

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

        def on_text_motion(motion):
            """World mode controls. User can move Hero to interact with other
            Entities in World, initiate Combat, and access the pause menu."""
            self.queued_input = motion

        def on_text(text):
            self.queued_input = text

        def on_key_press(symbol, modifiers):
            if symbol == self.pause_key:
                self.activate_pause_menu()

        self.on_draw = on_draw
        self.on_text_motion = on_text_motion
        self.on_text = on_text
        self.on_key_press = on_key_press

        pyglet.clock.schedule_interval(self.update_characters, self.base_delay)

    def activate_pause_menu(self):
        pyglet.clock.unschedule(self.update_characters)
        self.pause_menu.activate()

    def update_characters(self, dt):
        for character in self.world.get_characters():
            if character is self.hero:
                if self.queued_input in self.movement_keys.values():
                    self.hero_move()
                elif self.queued_input == self.interact_key:
                    self.hero_interact()
                self.queued_input = None
            else:
                self.npc_wander(character)

    # hero methods ------------------------------------------------------------
    def hero_move(self):
        x = 0
        y = 0
        if self.queued_input == self.movement_keys['left']:
            x = -1
        if self.queued_input == self.movement_keys['down']:
            y = -1
        if self.queued_input == self.movement_keys['up']:
            y = 1
        if self.queued_input == self.movement_keys['right']:
            x = 1

        self.world.step_hero(x, y)
        self.hero.direction = (x, y)

    def hero_interact(self):
        x_dir, y_dir = self.hero.direction
        x, y = self.world.get_coords(self.hero)
        interactable = self.world.get_interactable(x + x_dir, y + y_dir)
        if interactable:
            args = self.interact_args[str(interactable)]
            interactable.interact(*args)

    # npc methods -------------------------------------------------------------
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
            axis = random.choice(('x', 'y'))
            if axis == 'x':
                x_dir = random.choice((-1, 1))
                y_dir = 0
            else:
                y_dir = random.choice((-1, 1))
                x_dir = 0
            self.world.step_entity(character, x_dir, y_dir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout,
        format='%(levelname)s:%(message)s')

    game = Game()
    game.run()
