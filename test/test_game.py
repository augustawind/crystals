import pyglet

from crystals import game
from crystals import gui
from crystals import world

class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def test_init(self):
        assert isinstance(self.game.batch, pyglet.graphics.Batch)
        assert type(self.game.win_width) == int
        assert type(self.game.win_height) == int
        assert isinstance(self.game.window, pyglet.window.Window)
        assert isinstance(self.game.main_menu, gui.Menu)
        assert self.game.world == None

    def test_run(self):
        #self.game.run() # comment this line for ease of testing
        pass

    def test_new_game(self):
        self.game.new_game()
        assert isinstance(self.game.world, world.Room)
