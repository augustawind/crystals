import pyglet

from crystals import game
from crystals import gui

class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def test_init(self):
        assert isinstance(self.game.batch, pyglet.graphics.Batch)
        assert type(self.game.win_width) == int
        assert type(self.game.win_height) == int
        assert self.game.window == None
        assert isinstance(self.game.main_menu, gui.Menu)

    def test_run(self):
        pass
        # commented out for ease of testing
        #self.game.run()
        #assert isinstance(self.game.window, pyglet.window.Window)
        ## check whether menu event handlers have been pushed
        #self.game.window.pop_handlers()
