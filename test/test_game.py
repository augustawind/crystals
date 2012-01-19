import pyglet
from pyglet.window import key

from crystals import game
from crystals import gui
from crystals import entity
from crystals import world
from test.test_world import WorldTestCase
from test.helpers import *

class TestGameMode(object):

    def test_init(self):
        window = pyglet.window.Window()

        gamemode = game.GameMode(window)
        assert gamemode.window == window
        assert isinstance(gamemode.batch, pyglet.graphics.Batch)


class TestMainMenu(object):

    def test_init(self):
        window = pyglet.window.Window()
        new_game = lambda: None

        mm = game.MainMenu(window, new_game)
        assert mm.window == window
        assert isinstance(mm.batch, pyglet.graphics.Batch)
        assert mm.functions[0] == new_game


class TestWorldMode(WorldTestCase):

    def setup(self):
        WorldTestCase.setup(self)

        self.window = pyglet.window.Window()
        self.room1 = self.get_room()[0]
        self.room2 = self.get_room()[0]
        self.rooms = {'a room': self.room1, 'b room': self.room2}
        self.world_ = world.World(self.rooms, 'b room')
        self.player = entity.Entity(
            'character', 'player', False, pyglet.image.load(
            os.path.join(IMAGE_PATH, 'character', 'cow.png')))
        self.room2.add_entity(self.player, 1, 1, 1)
        self.worldmode = game.WorldMode(self.window, self.world_, self.player)

    def test_init(self):
        assert isinstance(self.worldmode, game.GameMode)
        assert self.worldmode.window == self.window
        assert self.worldmode.batch != self.worldmode.world.focus.batch
        assert self.worldmode.world == self.world_
        assert self.worldmode.player == self.player

    def test_activate(self):
        self.worldmode.activate()
        assert self.worldmode.batch == self.worldmode.world.focus.batch

    def test_on_text_motion(self):
        x1, y1 = self.worldmode.player.position
        self.worldmode.on_text_motion(key.MOTION_DOWN)
        x2, y2 = self.worldmode.player.position
        assert self.room2[1][2][1] == self.player
        assert x2 == x1 + world.TILE_SIZE
        assert y2 == y1 + world.TILE_SIZE


class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def test_init(self):
        assert type(self.game.win_width) == int
        assert type(self.game.win_height) == int
        assert isinstance(self.game.window, pyglet.window.Window)
        assert isinstance(self.game.main_menu, game.MainMenu)
        assert self.game.world == None
        assert self.game.player == None

    def test_run(self):
        pass
        #self.game.run() # Comment this line for ease of testing

    def test_new_game(self):
        self.game.window.push_handlers(self.game.main_menu)
        self.game.new_game()
        assert isinstance(self.game.world, game.WorldMode)
