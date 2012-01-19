from nose.tools import *

from crystals import world
from crystals import entity
from crystals.data import ImageDict
from test.helpers import *
from test.test_data import IMAGE_PATH

class WorldTestCase(TestCase):

    def __init__(self):
        super(WorldTestCase, self).__init__()
        self.img = ImageDict('terrain', IMAGE_PATH)

    def get_room(self):
        name = 'a room'
        wall = lambda: entity.Entity(
            'terrain', 'wall', False, self.img['wall-vert-blue'])
        floor = lambda: entity.Entity(
            'terrain', 'floor', True, self.img['floor-b-red'])
        layers = [
            [[wall(), wall(), wall()],
             [wall(), floor(), wall()],
             [wall(), floor(), floor()]],
            [[None, None, None],
             [None, None, None],
             [None, None, wall()]]]
        room = world.Room(name, self.batch, layers)
        room.focus()

        return room, name, layers, wall, floor


@raises(world.WorldError)
def test_WorldError():
    raise world.WorldError()


class TestRoom(WorldTestCase):

    def test_init(self):
        room, name, layers, wall, floor = self.get_room()
        assert room == layers
        assert isinstance(room.batch, pyglet.graphics.Batch)
        assert all(isinstance(group, pyglet.graphics.OrderedGroup)
                   for group in room.groups)

    def test__update_entity(self):
        room, name, layers, wall, floor = self.get_room()
        wall1 = wall()
        room._update_entity(wall1, 2, 1, 0)
        assert wall1.batch == room.batch
        assert wall1.x == world.ORIGIN_X + (2 * world.TILE_SIZE)
        assert wall1.y == world.ORIGIN_Y + world.TILE_SIZE
        assert wall1.group.order == 0

        floor1 = floor()
        room._update_entity(floor1, 0, 0, 0)
        assert floor1.batch == room.batch
        assert floor1.x == world.ORIGIN_X
        assert floor1.y == world.ORIGIN_Y
        assert floor1.group.order == 0

    def test_iswalkable(self):
        room = self.get_room()[0]
        assert not room.iswalkable(0, 0)
        assert room.iswalkable(1, 1)

    def test_focus(self):
        room = self.get_room()[0]
        room.focus()
        for layer in room:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    if layer[y][x] is None:
                        continue
                    assert layer[y][x].x == x * world.TILE_SIZE + world.ORIGIN_X
                    assert layer[y][x].y == y * world.TILE_SIZE + world.ORIGIN_Y

    def test_get_coords(self):
        room = self.get_room()[0]
        entity_ = room[0][0][0]
        x, y, z = room.get_coords(entity_)
        assert (x, y, z) == (0, 0, 0)

    def test_add_layer(self):
        room = self.get_room()[0]

        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer(0)
        assert len(room) == roomlen + 1
        assert len(room.groups) == grouplen + 1
        for group in room.groups:
            assert group.order == room.groups.index(group)

        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer()
        assert all(e == None for row in room[-1] for e in row)
        assert len(room.groups) == grouplen + 1
        for group in room.groups:
            assert group.order == room.groups.index(group)

    def dummy_entity(self):
        images = ImageDict('terrain', IMAGE_PATH)
        return entity.Entity('terrain', 'tree', False, images['tree-green'],
                             pyglet.graphics.Batch())

    def test_replace_entity(self):
        room = self.get_room()[0]
        dummy = self.dummy_entity()
        room.replace_entity(dummy, 0, 0, 0)
        assert room[0][0][0] == dummy

    def test_add_entity(self):
        room = self.get_room()[0]
        dummy = self.dummy_entity()

        room.add_entity(dummy, 1, 1, 1)
        assert room[1][1][1] == dummy 
        assert dummy.batch == room.batch
        assert dummy.group == room.groups[1]

    @raises(world.WorldError)
    def test_add_entity_is_safe(self):
        room = self.get_room()[0]
        room.add_entity(self.dummy_entity(), 0, 0, 0)



class TestWorld(WorldTestCase):

    def setup(self):
        super(TestWorld, self).setup()
        self.room1, n1, l1, self.wall1, self.floor1 = self.get_room()
        self.room2, n2, l2, self.wall2, self.floor2 = self.get_room()
        self.room2.name = 'b room'
        self.rooms = {'a room': self.room1, 'b room': self.room2}
        self.world = world.World(self.rooms, 'b room')

    def test_init(self):
        assert self.world == self.rooms
        assert self.world.focus == self.room2

    def test_add_entity1(self):
        wall = self.wall1()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1)
        assert self.world.focus[-1][1][1] == wall
        assert len(self.world.focus) == nlayers + 1

    def test_add_entity2(self):
        floor = self.floor1()
        nlayers = len(self.world.focus)
        self.world.add_entity(floor, 1, 1, 0)
        assert self.world.focus[0][1][1] == floor
        assert len(self.world.focus) == nlayers + 1

    def test_add_entity3(self):
        wall = self.wall2()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1, 1)
        assert self.world.focus[1][1][1] == wall
        assert len(self.world.focus) == nlayers

    def test_pop_entity(self):
        entity_ = self.world.pop_entity(0, 0, 0)
        assert entity_.name == self.wall2().name
        assert self.world.focus[0][0][0] == None

    def test_step_entity(self):
        entity_ = self.room2[0][0][0]
        self.world.step_entity(entity_, 1, 2)
        assert self.room2[0][2][1] == entity_
