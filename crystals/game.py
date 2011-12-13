"""top-level application logic"""

import random

import pyglet
from pyglet.window import key, mouse

import data
import interface
from world import \
    VIEWPORT_ROWS, VIEWPORT_COLS, OFFSET_ROWS, OFFSET_COLS, TILE_SIZE

class Game(pyglet.window.Window):
    """The main application class. Runs the game!"""

    def __init__(self):
        super(Game, self).__init__(
            (VIEWPORT_COLS + OFFSET_COLS) * TILE_SIZE,
            (VIEWPORT_ROWS + OFFSET_ROWS) * TILE_SIZE,
            caption='CRYSTALS', resizable=False)
        
        self.main_menu = interface.MainMenu(self)
        self.pause_menu = None
        self.message_box = None

        self.world = None
        self.combat = None
        self.hero = None

        # application variables -----------------------------------------------
        self.base_delay = 0.001
        self.wander_frequency = 0.05
        self.queued_input = None

        # dict of argument tuples for calls to Interactable.interact,
        # indexed by str(Interactable)
        self.interact_args = {
            'text': (self.message_box, ),
            'talk': (self.message_box, )}

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
        self.pause_menu = interface.PauseMenu(self)

        self.activate_world_mode()

    def load_game(self):
        pass

    def quit(self):
        pyglet.app.exit()

    # combat mode methods
    # -------------------------------------------------------------------------

    def activate_combat_mode(self):
        pass

    # world mode methods
    # -------------------------------------------------------------------------

    def activate_world_mode(self):
        #self.message_box = interface.MessageBox(self)

        def on_draw():
            self.clear()
            #self.message_box.draw()
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

        self.pop_handlers()
        self.push_handlers(on_draw, on_text_motion, on_text, on_key_press)

        pyglet.clock.schedule_interval(self.update_characters, self.base_delay)

    def activate_pause_menu(self):
        pyglet.clock.unschedule(self.update_characters)
        self.pop_handlers()
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

    def hero_interact(self):
        print 'game.hero_interact'
        xdir, ydir = self.hero.direction
        x, y = self.world.get_coords(self.hero)
        interactions = self.world.get_interactions(x + xdir, y + ydir)
        print 'interactions =', interactions
        if interactions:
            for interaction in interactions:
                args = self.interact_args[str(interaction)]
                interaction.interact(*args)
        print

    # npc methods -------------------------------------------------------------
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
