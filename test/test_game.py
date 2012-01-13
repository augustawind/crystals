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

    def test_init(self):
        window = pyglet.window.Window()
        room1 = self.get_room()[0]
        room2 = self.get_room()[0]
        rooms = {'a room': room1, 'b room': room2}

        worldmode = game.WorldMode(window, rooms, 'b room')
        assert worldmode.window == window
        assert isinstance(worldmode, game.GameMode)
        assert isinstance(worldmode, world.World)


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
        #self.game.run() # comment this line for ease of testing

    def test_new_game(self):
        self.game.window.push_handlers(self.game.main_menu)
        self.game.new_game()
        assert isinstance(self.game.world, world.Room)
