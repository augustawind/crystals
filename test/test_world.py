from crystals import world
from crystals import entity
from crystals.loaders import ImageDict

from test.helpers import *

class TestRoom(TestCase):

    def setup(self):
        super(TestRoom, self).setup()
        img = ImageDict('terrain')
        self.wall = entity.Entity(
            'terrain', 'wall', False, img['wall-vert-blue'])
        self.floor = entity.Entity(
            'terrain', 'floor', True, img['floor-b-blue'])
        self.grid = [[self.wall, self.wall, self.wall],
                [self.wall, self.floor, self.wall],
                [self.wall, self.floor, self.floor]]
        self.room = world.Room(self.grid, self.batch)

    def test_init(self):
        assert self.room == self.grid
        assert self.room.batch == self.batch
