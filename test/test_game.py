import pyglet

from crystals import game
from crystals import gui
from crystals import world

class TestGameMode(object):

    def test_init(self):
        window = pyglet.window.Window()
        batch = pyglet.graphics.Batch()

        gamemode = game.GameMode(window, batch)
        assert gamemode.window == window
        assert gamemode.batch == batch


class TestMainMenu(object):

    def test_init(self):
        window = pyglet.window.Window()
        batch = pyglet.graphics.Batch()
        new_game = lambda: None

        mm = game.MainMenu(window, batch, new_game)
        assert mm.window == window
        assert mm.batch == batch
        assert mm.functions[0] == new_game


class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def test_init(self):
        assert isinstance(self.game.batch, pyglet.graphics.Batch)
        assert type(self.game.win_width) == int
        assert type(self.game.win_height) == int
        assert isinstance(self.game.window, pyglet.window.Window)
        assert isinstance(self.game.main_menu, game.MainMenu)
        assert self.game.world == None

    def test_run(self):
        #self.game.run() # comment this line for ease of testing
        pass

    def test_new_game(self):
        self.game.window.push_handlers(self.game.main_menu)
        self.game.new_game()
        assert isinstance(self.game.world, world.Room)
