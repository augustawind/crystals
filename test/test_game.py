import pyglet

from crystals import game
from crystals import gui
from crystals import world
from test.test_world import WorldTestCase

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
        self.worldmode = game.WorldMode(self.window, self.world_)

    def test_init(self):
        assert self.worldmode.window == self.window
        assert self.worldmode.batch != self.worldmode.world.focus.batch
        assert self.worldmode.world == self.world_
        assert isinstance(self.worldmode, game.GameMode)

    def test_activate(self):
        self.worldmode.activate()
        assert self.worldmode.batch == self.worldmode.world.focus.batch


class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def test_init(self):
        assert type(self.game.win_width) == int
        assert type(self.game.win_height) == int
        assert isinstance(self.game.window, pyglet.window.Window)
        assert isinstance(self.game.main_menu, game.MainMenu)
        assert self.game.world == None

    def test_run(self):
        pass
        #self.game.run() # Comment this line for ease of testing

    def test_new_game(self):
        self.game.window.push_handlers(self.game.main_menu)
        self.game.new_game()
        assert isinstance(self.game.world, game.WorldMode)
