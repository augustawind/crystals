from crystals import world
from crystals import entity
from crystals.loaders import ImageDict

from test.helpers import *

class TestRoom(TestCase):

    def test_init(self):
        img = ImageDict('terrain')
        wall = entity.Entity('wall', False, img['wall-vert-blue'], self.batch)
        floor = entity.Entity('floor', True, img['floor-b-blue'], self.batch)
        grid = [[wall, wall, wall],
                [wall, floor, wall],
                [wall, floor, floor]]
        room = world.Room(grid, self.batch)
        assert room == grid
        assert room.batch == self.batch
