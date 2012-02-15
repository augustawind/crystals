import pyglet
from pyglet.window import key

from crystals import game
from crystals import gui
from crystals import world
from crystals.test.util import *


class TestGame(object):

    def TestInit(self):
        game_ = game.Game()

    def TestNewGame_LoadWorldMode(self):
        game_ = game.Game()
        def on_draw():
            pass
        game_.window.push_handlers(on_draw)
        game_.new_game()
        assert isinstance(game_.wmode, game.WorldMode)
