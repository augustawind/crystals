from crystals import world
from crystals import entity
from crystals.loaders import ImageDict

from test.helpers import *

class WorldTestCase(TestCase):

    def __init__(self):
        super(WorldTestCase, self).__init__()
        self.img = ImageDict('terrain')

    def get_room(self):
        wall = lambda: entity.Entity(
            'terrain', 'wall', False, self.img['wall-vert-blue'])
        floor = lambda: entity.Entity(
            'terrain', 'floor', True, self.img['floor-b-blue'])
        layers = [
            [[wall(), wall(), wall()],
             [wall(), floor(), wall()],
             [wall(), floor(), floor()]]]
        room = world.Room(self.batch, layers)

        return room, layers, wall, floor


class TestRoom(WorldTestCase):

    def test_init(self):
        room, layers, wall, floor = self.get_room()
        assert room == layers
        assert room.batch == self.batch

        for layer in room:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    assert layer[y][x].x == x * world.TILE_SIZE
                    assert layer[y][x].y == y * world.TILE_SIZE

    def test__update_entity(self):
        room, layers, wall, floor = self.get_room()
        wall1 = wall()
        room._update_entity(wall1, 2, 1)
        assert wall1.batch == room.batch
        assert wall1.x == 2 * world.TILE_SIZE
        assert wall1.y == 1 * world.TILE_SIZE

        floor1 = floor()
        room._update_entity(floor1, 0, 0)
        assert floor1.batch == room.batch
        assert floor1.x == 0
        assert floor1.y == 0

class TestWorld(WorldTestCase):

    def setup(self):
        super(TestWorld, self).setup()
        self.room1, l1, self.wall1, self.floor1 = self.get_room()
        self.room2, l2, self.wall2, self.floor2 = self.get_room()
        self.room2 = reversed(self.room2)
        self.world = world.World(self.batch, [self.room1, self.room2], 1)

    def test_init(self):
        assert self.world == [self.room1, self.room2]
        assert self.world.batch == self.batch
        assert self.world.focus == 1
