import pyglet
from pyglet.window import key

from crystals import game
from crystals import gui
from crystals import entity
from crystals import world
from test.util import *
from test.test_world import WorldTestCase
from test.test_resource import imgloader

images = imgloader()

class TestGameMode(object):

    def TestInit_AttrsHaveExpectedValues(self):
        window = pyglet.window.Window()
        gamemode = game.GameMode(window)
        assert gamemode.window == window
        assert isinstance(gamemode.batch, pyglet.graphics.Batch)


class TestMainMenu(object):

    def TestInit_AttrsHaveExpectedValues(self):
        window = pyglet.window.Window()
        new_game = lambda: None
        mm = game.MainMenu(window, new_game)
        assert mm.functions[0] == new_game


class TestWorldMode(WorldTestCase):

    def setup(self):
        WorldTestCase.setup(self)

        self.window = pyglet.window.Window()
        self.room1 = self.roomgen.next()
        self.room2 = self.roomgen.next()
        self.rooms = {self.room1.name: self.room1, self.room2.name: self.room2}

        self.portals = {
            self.room1.name: [ 
                ['', '', ''],
                ['', '', ''],
                ['', self.room2.name, '']],
            self.room2.name: [ 
                ['', '', ''],
                ['', self.room1.name, ''],
                ['', '', '']]}

        self.world_ = world.World(self.rooms, self.portals,
                                  self.room2.name)
        self.player = entity.Entity('player', False, images.image('cow.png'),
                                    pos=(0, -1))
        self.room2.add_entity(self.player, 1, 1, 1)
        self.worldmode = game.WorldMode(self.window, self.world_, self.player)

    def TestInit_AttrsHaveExpectedValues(self):
        assert isinstance(self.worldmode, game.GameMode)
        assert self.worldmode.window == self.window
        assert self.worldmode.batch == self.worldmode.world.focus.batch
        assert self.worldmode.world == self.world_
        assert self.worldmode.player == self.player

    def TestActivate_Exists(self):
        self.worldmode.activate()

    def TestStepPlayer_NoPortalAtDest_MovePlayerGivenDistance(self):
        self.worldmode.step_player(0, 1)
        assert self.room2[1][2][1] == self.player

    def TestStepPlayer_PortalAtDest_MovePlayerToPortalDest(self):
        self.worldmode.step_player(0, 1)
        self.worldmode.step_player(0, -1)
        assert self.room2[1][1][1] != self.player
        assert self.room1[1][2][1] == self.player

    def TestPortalPlayer_ValidCoordsGiven_AddPlayerToPortalDest(self):
        x, y, z = self.room2.get_coords(self.worldmode.player)
        self.worldmode.portal_player(x, y)
        x, y = self.world_.get_dest_portal_xy(self.room1.name, self.room2.name)
        assert self.room1[z][y][x] == self.worldmode.player

    def TestPortalPlayer_ValidCoordsGiven_DelPlayerFromPrevPos(self):
        x, y, z = self.room2.get_coords(self.worldmode.player)
        self.worldmode.portal_player(x, y)
        assert self.room2[z][y][x] != self.worldmode.player

    def TestPortalPlayer_ValidCoordsGiven_SetFocusToNewRoom(self):
        x, y, z = self.room2.get_coords(self.worldmode.player)
        self.worldmode.portal_player(x, y)
        assert self.world_.focus == self.room1

    def TestInteract_AlertAction_ActionExecutes(self):
        self.worldmode.interact()

    def TestOnKeyPress_MovementKeyPressedAndWalkable_MovePlayer(self):
        x, y, z = self.world_.focus.get_coords(self.worldmode.player)
        self.worldmode.on_key_press(key.MOTION_UP, 0)
        assert self.room2[z][y + 1][x] == self.player

    def TestOnKeyPress_MovementKeyPressedButUnWalkable_DoNothing(self):
        for mvkey in (key.MOTION_LEFT, key.MOTION_DOWN, key.MOTION_RIGHT):
            x, y, z = self.world_.focus.get_coords(self.worldmode.player)
            self.worldmode.on_key_press(mvkey, 0)
            assert self.room2[z][y][x] == self.player


class TestGame(object):

    def setup(self):
        self.game = game.Game()

    def TestInit_AttrsHaveExpectedValues(self):
        assert isinstance(self.game.window, pyglet.window.Window)
        assert isinstance(self.game.main_menu, game.MainMenu)
        assert self.game.world == None
        assert self.game.player == None

    def TestNewGame_LoadWorld(self):
        self.game.main_menu.activate()
        self.game.new_game()
        assert isinstance(self.game.world, game.WorldMode)
