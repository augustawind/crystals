from itertools import count
from functools import partial

import pyglet
from nose.tools import *

from crystals import world
from test.util import *
from test.test_resource import imgloader


class MockEntity(pyglet.sprite.Sprite):

    def __init__(self, name='entity', walkable=True, actions=[]):
        pyglet.sprite.Sprite.__init__(
            self, imgloader().image('cow.png'),
            batch=pyglet.graphics.Batch())
        self.name = name
        self.walkable = walkable
        self.actions = actions
        self.id = id(self)


class WorldTestCase(object):

    def __init__(self):
        super(WorldTestCase, self).__init__()

    def setup(self):
        self.roomgen = self.getrooms()

    def getrooms(self):
        for i in count(0):
            self.rm_name = 'room{}'.format(i)
            self.Wall = partial(MockEntity, 'wall{}'.format(i), False)
            self.Floor = partial(MockEntity, 'floor{}'.format(i), True)
            self.rm_layers = [
                [[self.Wall(), self.Wall(), self.Wall()],
                 [self.Wall(), self.Floor(), self.Wall()],
                 [self.Wall(), self.Floor(), self.Floor()]],
                [[None, None, None],
                 [None, None, None],
                 [None, None, self.Wall()]],
                [[self.Floor(), self.Floor(), self.Floor()],
                 [self.Floor(), self.Floor(), self.Floor()],
                 [self.Floor(), self.Floor(), self.Wall()]]]
            self.grid = [
                [list(row) for row in zip(*rows)]
                 for rows in zip(*self.rm_layers)]
            self.batch = pyglet.graphics.Batch()

            room = world.Room(self.rm_name, self.grid)
            room.batch = self.batch
            room.update()
            yield room


@raises(world.WorldError)
def TestWorldError():
    raise world.WorldError()


class TestRoom(WorldTestCase):

    def TestInit_UniquesIndexed(self):
        room = self.roomgen.next()
        assert len(room.uniques) == len([
            0 for row in self.grid for col in row for cell in col if cell])

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

    def TestIsWalkable_GivenOutOfBoundsCoords_ReturnFalse(self):
        room = self.roomgen.next()
        assert not room.iswalkable(len(room[0]), len(room))

    def TestFocus_UpdateEntitySpritePositionsAndBatches(self):
        room = self.roomgen.next()
        room.update()
        for y in xrange(len(room)):
            for x in xrange(len(room[y])):
                for z in xrange(len(room[y][x])):
                    ent = room[y][x][z]
                    if ent is None:
                        continue
                    assert ent.x == x * world.TILE_SIZE + world.ORIGIN_X
                    assert ent.y == y * world.TILE_SIZE + world.ORIGIN_Y
                    assert ent.batch is room.batch

    def TestGetCoords_GivenValidEntity_ReturnEntityCoords(self):
        room = self.roomgen.next()
        entity_ = room[0][0][0]
        x, y, z = room.get_coords(entity_)

        assert (x, y, z) == (0, 0, 0)

    def _group_order_matches_z(self, room, x, y):
        for z, entity in enumerate(room[y][x]):
            if entity and entity.group.order != z:
                return False
        return True

    def TestReplaceEntity_EntityAtDest_ReplaceWithNewEntity(self):
        room = self.roomgen.next()
        dummy = MockEntity()
        room.replace_entity(dummy, 0, 0, 0)
        assert room[0][0][0] == dummy


class TestWorld(WorldTestCase):

    def setup(self):
        WorldTestCase.setup(self)

        self.rooms = []
        self.roomdict = {}
        self.walls = []
        self.floors = []
        for i in xrange(2):
            room = self.roomgen.next()
            self.rooms.append(room)
            self.roomdict[room.name] = room
            self.walls.append(self.Wall)
            self.floors.append(self.Floor)

        self.portals = {
            self.rooms[0].name: {
                self.rooms[1].name: (1, 2)},
            self.rooms[1].name: {
                self.rooms[0].name: (1, 1)}}

        self.world = world.World(self.roomdict, self.portals, 'room1') 

    def TestInit_AttrsHaveExpectedValues(self):
        assert self.world == self.roomdict
        assert self.world.focus == self.rooms[1]

    def TestAddEntity_ZIsNone_AddLayerToTopAndPlaceThere(self):
        wall = self.walls[0]()
        x = y = 1
        cell = self.world.focus[y][x]
        depth = len(cell)
        self.world.add_entity(wall, x, y, None)
        assert len(cell) == depth + 1
        assert cell[-1] == wall

    def TestAddEntity_ZOutOfRange_AddLayerToTopAndPlaceThere(self):
        wall = self.walls[1]()
        x = y = z = 1
        cell = self.world.focus[y][x]
        depth = len(cell)
        self.world.add_entity(wall, x, y, z)
        assert len(cell) == depth
        assert cell[z] == wall

    def TestAddEntity_ZInRangeAndEntityAtXYZ_AddLayerAboveZAndPlaceThere(self):
        floor = self.floors[0]()
        x = y = 1
        z = 0
        cell = self.world.focus[y][x]
        depth = len(cell)
        self.world.add_entity(floor, x, y, z)
        assert len(cell) == depth + 1
        assert cell[1] == floor

    def TestAddEntity_ZInRangeAndEntityAtXYZ_UpdateAboveEntityGroups(self):
        floor = self.floors[0]()
        x = y = 1
        z = 0
        cell = self.world.focus[y][x]
        self.world.add_entity(floor, x, y, z)

        for ent in cell:
            if ent:
                assert ent.group.order == cell.index(ent)

    def TestPopEntity_EntityCoordsGiven_RemoveEntity(self):
        self.world.pop_entity(0, 0, 0)
        assert self.world.focus[0][0][0] == None

    def TestPopEntity_EntityCoordsGiven_ReturnEntity(self):
        entity_ = self.world.pop_entity(0, 0, 0)
        assert entity_.name == self.walls[1]().name

    def TestStepEntity_WalkableCoordsGiven_ChangeEntityPos(self):
        entity_ = self.rooms[1][0][0][0]
        positions = ((1, 0), (-1, 0), (0, -1))
        for fx, fy in positions:
            self.world.step_entity(entity_, fx, fy)
            assert entity_.facing == (fx, fy)

    def TestStepEntity_UnwalkableCoordsGiven_ChangeEntityPos(self):
        entity_ = self.rooms[1][0][0][0]
        fx, fy = 0, 1
        self.world.step_entity(entity_, fx, fy)
        assert entity_.facing == (fx, fy)

    def TestStepEntity_DestWalkable_MoveEntity(self):
        entity_ = self.rooms[1][0][0][0]
        self.world.step_entity(entity_, 1, 2)
        assert self.rooms[1][0][0][0] != entity_
        assert self.rooms[1][2][1][1] == entity_

    def TestStepEntity_DestWalkable_ReturnTrue(self):
        entity_ = self.rooms[1][0][0][0]
        assert self.world.step_entity(entity_, 1, 2)

    def TestStepEntity_DestUnwalkable_DontMoveEntity(self):
        entity_ = self.rooms[1][0][0][0]
        self.world.step_entity(entity_, -1, 0)
        assert self.rooms[1][0][0][0] == entity_

    def TestStepEntity_DestUnwalkable_ReturnFalse(self):
        entity_ = self.rooms[1][0][0][0]
        assert not self.world.step_entity(entity_, -1, 0)

    def TestPortalEntity_GivenValidInputs_MoveEntityToPortalDest(self):
        x, y, z = (1, 1, 0)
        entity_ = self.rooms[1][y][x][z]
        self.world.portal_entity(entity_, 1, 1)
        assert self.rooms[1][y][x][z] != entity_

        x, y, z = self.rooms[0].get_coords(entity_)
        assert self.rooms[0][y][x][z] == entity_
