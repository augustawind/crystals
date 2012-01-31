from itertools import count

from nose.tools import *

from crystals import world
from crystals import entity
from crystals.data import ImageDict
from test.util import *
from test.test_data import IMAGE_PATH


class WorldTestCase(object):

    def __init__(self):
        super(WorldTestCase, self).__init__()

    def setup(self):
        self.roomgen = self.getroom()

    def getroom(self):
        for i in count(0):
            self.imagedict = ImageDict('terrain', IMAGE_PATH)
            self.rm_name = 'room{}'.format(i)
            self.Wall = lambda: entity.Entity(
                'terrain', 'wall{}'.format(i), False,
                self.imagedict['wall-vert-blue'])
            self.Floor = lambda: entity.Entity(
                'terrain', 'floor{}'.format(i), True,
                 self.imagedict['floor-b-red'])
            self.rm_layers = [
                [[self.Wall(), self.Wall(), self.Wall()],
                 [self.Wall(), self.Floor(), self.Wall()],
                 [self.Wall(), self.Floor(), self.Floor()]],
                [[None, None, None],
                 [None, None, None],
                 [None, None, self.Wall()]]]
            self.batch = pyglet.graphics.Batch()

            room = world.Room(self.rm_name, self.batch, self.rm_layers)
            room.focus()
            yield room


@raises(world.WorldError)
def test_WorldError():
    raise world.WorldError()


class TestRoom(WorldTestCase):

    def TestInit_AttrsHaveExpectedValues(self):
        room = self.roomgen.next()

        assert room == self.rm_layers
        assert room.batch == self.batch
        for group in room.groups:
            assert isinstance(group, pyglet.graphics.OrderedGroup)

    def TestUpdateEntity_ValidInputs_AddEntityToRoomBatch(self):
        room = self.roomgen.next()
        wall = self.Wall()
        room._update_entity(wall, 2, 1, 0)
        assert wall.batch == room.batch

    def TestUpdateEntity_ValidInputs_UpdateSpriteCoords(self):
        room = self.roomgen.next()
        wall = self.Wall()
        room._update_entity(wall, 2, 1, 0)
        assert wall.x == world.ORIGIN_X + (2 * world.TILE_SIZE)
        assert wall.y == world.ORIGIN_Y + world.TILE_SIZE

    def TestUpdateEntity_ValidInputs_UpdateOrderedGroup(self):
        room = self.roomgen.next()
        wall = self.Wall()
        room._update_entity(wall, 2, 1, 0)
        assert wall.group.order == 0

    def TestIsWalkable_GivenWalkableCoords_ReturnTrue(self):
        room = self.roomgen.next()
        assert room.iswalkable(1, 1)

    def TestIsWalkable_GivenUnwalkableCoords_ReturnFalse(self):
        room = self.roomgen.next()
        assert not room.iswalkable(0, 0)

    def TestFocus_UpdateEntitySpritePositions(self):
        room = self.roomgen.next()
        room.focus()
        for layer in room:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    if layer[y][x] is None:
                        continue
                    assert layer[y][x].x == x * world.TILE_SIZE + world.ORIGIN_X
                    assert layer[y][x].y == y * world.TILE_SIZE + world.ORIGIN_Y

    def TestGetCoords_GivenValidEntity_ReturnEntityCoords(self):
        room = self.roomgen.next()
        entity_ = room[0][0][0]
        x, y, z = room.get_coords(entity_)
        assert (x, y, z) == (0, 0, 0)

    def test_add_layer(self):
        room = self.roomgen.next()
        
        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer(0)
        assert len(room) == roomlen + 1
        assert len(room.groups) == grouplen + 1
        for group in room.groups:
            assert group.order == room.groups.index(group)

        for z in (None, len(room)):
            roomlen = len(room)
            grouplen = len(room.groups)
            room.add_layer(z)
            assert all(e == None for row in room[-1] for e in row)
            assert len(room.groups) == grouplen + 1
            for group in room.groups:
                assert group.order == room.groups.index(group)

    def dummy_entity(self):
        images = ImageDict('terrain', IMAGE_PATH)
        return entity.Entity('terrain', 'tree', False, images['tree-green'],
                             pyglet.graphics.Batch())

    def test_replace_entity(self):
        room = self.roomgen.next()
        dummy = self.dummy_entity()
        room.replace_entity(dummy, 0, 0, 0)
        assert room[0][0][0] == dummy

    def test_add_entity(self):
        room = self.roomgen.next()
        dummy = self.dummy_entity()

        room.add_entity(dummy, 1, 1, 1)
        assert room[1][1][1] == dummy 
        assert dummy.batch == room.batch
        assert dummy.group == room.groups[1]

    @raises(world.WorldError)
    def test_add_entity_is_safe(self):
        room = self.roomgen.next()
        room.add_entity(self.dummy_entity(), 0, 0, 0)


class TestPortal(WorldTestCase):

    def test_init(self):
        from_room = self.roomgen.next()
        to_room = self.roomgen.next()
        portal = world.Portal(0, 0, from_room, to_room)


class TestWorld(WorldTestCase):

    def setup(self):
        WorldTestCase.setup(self)

        self.rooms = []
        self.roomdict = {}
        self.walls = []
        self.floors = []
        for i in range(2):
            room = self.roomgen.next()
            self.rooms.append(room)
            self.roomdict[room.name] = room
            self.walls.append(self.Wall)
            self.floors.append(self.Floor)

        self.portals = [world.Portal(1, 2, self.rooms[0], self.rooms[1]),
                        world.Portal(1, 1, self.rooms[1], self.rooms[0])]

        self.world = world.World(self.roomdict, self.portals, 'room1') 

    def test_init(self):
        assert self.world == self.roomdict
        assert self.world.focus == self.rooms[1]

    def test_get_portal(self):
        assert self.world.get_portal(1, 1) == self.portals[1]
        assert self.world.get_portal(1, 2) == None
        assert self.world.get_portal(1, 2, room=self.rooms[0]) == self.portals[0]

    def test_add_entity1(self):
        wall = self.walls[0]()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1)
        assert self.world.focus[-1][1][1] == wall
        assert len(self.world.focus) == nlayers + 1

    def test_add_entity2(self):
        floor = self.floors[0]()
        nlayers = len(self.world.focus)
        self.world.add_entity(floor, 1, 1, 0)
        assert self.world.focus[1][1][1] == floor
        assert len(self.world.focus) == nlayers + 1

    def test_add_entity3(self):
        wall = self.walls[1]()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1, 1)
        assert self.world.focus[1][1][1] == wall
        assert len(self.world.focus) == nlayers

    def test_pop_entity(self):
        entity_ = self.world.pop_entity(0, 0, 0)
        assert entity_.name == self.walls[1]().name
        assert self.world.focus[0][0][0] == None

    def test_step_entity_changes_pos(self):
        entity_ = self.rooms[1][0][0][0]
        positions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for posx, posy in positions:
            self.world.step_entity(entity_, posx, posy)
            assert entity_.pos == (posx, posy)

    def test_step_entity_moves_entity_dest_walkable(self):
        entity_ = self.rooms[1][0][0][0]
        self.world.step_entity(entity_, 1, 2)
        assert self.rooms[1][0][0][0] != entity_
        assert self.rooms[1][1][2][1] == entity_

    def test_step_entity_doesnt_move_entity_dest_unwalkable(self):
        entity_ = self.rooms[1][0][0][0]
        self.world.step_entity(entity_, -1, 0)
        assert self.rooms[1][0][0][0] == entity_

    def test_step_entity_returns_true_dest_walkable(self):
        entity_ = self.rooms[1][0][0][0]
        assert self.world.step_entity(entity_, 1, 2)

    def test_step_entity_returns_false_dest_unwalkable(self):
        entity_ = self.rooms[1][0][0][0]
        stepped = self.world.step_entity(entity_, -1, 0)
        assert not stepped

    def test_portal_entity(self):
        x, y, z = (1, 1, 0)
        entity_ = self.rooms[1][z][y][x]
        self.world.portal_entity(entity_, self.portals[1])
        assert self.rooms[1][z][y][x] != entity_
        x, y, z = self.rooms[0].get_coords(entity_)
        assert self.rooms[0][z][y][x] == entity_
