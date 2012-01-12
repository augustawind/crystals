from crystals import world
from crystals import entity
from crystals.loaders import ImageDict

from test.helpers import *

class TestRoom(TestCase):

    def setup(self):
        super(TestRoom, self).setup()
        img = ImageDict('terrain')
        self.wall = lambda: entity.Entity(
            'terrain', 'wall', False, img['wall-vert-blue'])
        self.floor = lambda: entity.Entity(
            'terrain', 'floor', True, img['floor-b-blue'])
        self.grid = [
            [[self.wall(), self.wall(), self.wall()],
             [self.wall(), self.floor(), self.wall()],
             [self.wall(), self.floor(), self.floor()]]]
        self.room = world.Room(self.grid, self.batch)

    def test_init(self):
        assert self.room == self.grid
        assert self.room.batch == self.batch

        for layer in self.room:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    assert layer[y][x].x == x * world.TILE_SIZE
                    assert layer[y][x].y == y * world.TILE_SIZE

    def test_update_entity(self):
        wall = self.wall()
        self.room._update_entity(wall, 1, 2)
        assert wall.batch == self.room.batch
        assert wall.x == 1 * world.TILE_SIZE
        assert wall.y == 2 * world.TILE_SIZE
