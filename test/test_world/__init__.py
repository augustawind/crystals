from itertools import count

from nose.tools import *

from crystals import world
from crystals import entity
from test.util import *
from test.test_resource import imgloader

images = imgloader()


class WorldTestCase(object):

    def __init__(self):
        super(WorldTestCase, self).__init__()

    def setup(self):
        self.roomgen = self.getrooms()

    def getrooms(self):
        for i in count(0):
            self.rm_name = 'room{}'.format(i)
            self.Wall = lambda: entity.Entity(
                'wall{}'.format(i), False, images.image('wall-vert-blue.png'))
            self.Floor = lambda: entity.Entity(
                'floor{}'.format(i), True, images.image('floor-b-red.png'))
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
def TestWorldError():
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

    def _layer_is_empty(self, layer):
        for y in range(len(layer)):
            for x in range(len(layer[y])):
                if layer[y][x] is not None:
                    return False
        return True
    
    def _group_order_matches_index(self, room):
        for group in room.groups:
            if group.order != room.groups.index(group):
                return False
        return True

    def TestAddLayer_ZWithinCurrentNLayers_AddLayer(self):
        room = self.roomgen.next()
        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer(0)

        assert len(room) == roomlen + 1
        assert len(room.groups) == grouplen + 1
        assert self._layer_is_empty(room[0])
        assert self._group_order_matches_index(room)

    def TestAddLayer_ZIsNone_AppendLayerToTop(self):
        room = self.roomgen.next()
        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer(None)

        assert len(room) == roomlen + 1
        assert len(room.groups) == grouplen + 1
        assert self._layer_is_empty(room[-1])
        assert self._group_order_matches_index(room)

    def TestAddLayer_ZIsGTCurrentNLayer_AppendLayerToTop(self):
        room = self.roomgen.next()
        roomlen = len(room)
        grouplen = len(room.groups)
        room.add_layer(len(room))

        assert len(room) == roomlen + 1
        assert len(room.groups) == grouplen + 1
        assert self._layer_is_empty(room[-1])
        assert self._group_order_matches_index(room)

    def _DummyEntity(self):
        return entity.Entity(
            'tree', False, images.image('tree-green.png'),
            pyglet.graphics.Batch())

    def TestReplaceEntity_EntityAtDest_ReplaceWithNewEntity(self):
        room = self.roomgen.next()
        dummy = self._DummyEntity()
        room.replace_entity(dummy, 0, 0, 0)
        assert room[0][0][0] == dummy

    def TestAddEntity_NoEntityAtDest_PlaceEntityAtGivenDest(self):
        room = self.roomgen.next()
        dummy = self._DummyEntity()
        room.add_entity(dummy, 1, 1, 1)
        assert room[1][1][1] == dummy 

    @raises(world.WorldError)
    def TestAddEntity_EntityAtDest_RaiseWorldError(self):
        room = self.roomgen.next()
        dummy = self._DummyEntity()
        room.add_entity(dummy, 0, 0, 0)


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

        self.portals = {
            self.rooms[0].name: [ 
                ['', '', ''],
                ['', '', ''],
                ['', self.rooms[1].name, '']],
            self.rooms[1].name: [ 
                ['', '', ''],
                ['', self.rooms[0].name, ''],
                ['', '', '']]}

        self.world = world.World(self.roomdict, self.portals, 'room1') 

    def TestInit_AttrsHaveExpectedValues(self):
        assert self.world == self.roomdict
        assert self.world.focus == self.rooms[1]

    def TestGetPortalDestFromXY_PortalAtCoords_ReturnPortal(self):
        x = 1
        y = 1
        destname = self.world.get_portal_dest_from_xy(x, y)
        assert destname == self.portals[self.rooms[1].name][y][x]

    def TestGetPortalDestFromXY_NoPortalAtCoords_ReturnNone(self):
        assert self.world.get_portal_dest_from_xy(1, 2) == None

    def TestGetPortalDestFromXY_OtherRoomGiven_ReturnPortal(self):
        x = 1
        y = 2
        destname = self.world.get_portal_dest_from_xy(x, y, self.rooms[0].name)
        assert destname == self.portals[self.rooms[0].name][y][x]

    def TestGetPortalXYFromDest_PortalToDestExists_ReturnPortalXY(self):
        room = self.rooms[0].name
        x, y = self.world.get_portal_xy_from_dest(room)
        assert self.portals[self.rooms[1].name][y][x] == room

    def TestAddEntity_ZIsNone_AddLayerToTopAndPlaceThere(self):
        wall = self.walls[0]()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1, None)
        assert len(self.world.focus) == nlayers + 1
        assert self.world.focus[-1][1][1] == wall

    def TestAddEntity_ZOutOfRange_AddLayerToTopAndPlaceThere(self):
        wall = self.walls[1]()
        nlayers = len(self.world.focus)
        self.world.add_entity(wall, 1, 1, 1)
        assert len(self.world.focus) == nlayers
        assert self.world.focus[1][1][1] == wall

    def TestAddEntity_ZInRangeAndEntityAtXYZ_AddLayerAboveZAndPlaceThere(self):
        floor = self.floors[0]()
        nlayers = len(self.world.focus)
        self.world.add_entity(floor, 1, 1, 0)
        assert len(self.world.focus) == nlayers + 1
        assert self.world.focus[1][1][1] == floor

    def TestPopEntity_EntityCoordsGiven_RemoveEntity(self):
        self.world.pop_entity(0, 0, 0)
        assert self.world.focus[0][0][0] == None

    def TestPopEntity_EntityCoordsGiven_ReturnEntity(self):
        entity_ = self.world.pop_entity(0, 0, 0)
        assert entity_.name == self.walls[1]().name

    def TestStepEntity_WalkableCoordsGiven_ChangeEntityPos(self):
        entity_ = self.rooms[1][0][0][0]
        positions = ((1, 0), (-1, 0), (0, -1))
        for posx, posy in positions:
            self.world.step_entity(entity_, posx, posy)
            assert entity_.pos == (posx, posy)

    def TestStepEntity_UnwalkableCoordsGiven_ChangeEntityPos(self):
        entity_ = self.rooms[1][0][0][0]
        posx, posy = 0, 1
        self.world.step_entity(entity_, posx, posy)
        assert entity_.pos == (posx, posy)

    def TestStepEntity_DestWalkable_MoveEntity(self):
        entity_ = self.rooms[1][0][0][0]
        self.world.step_entity(entity_, 1, 2)
        assert self.rooms[1][0][0][0] != entity_
        assert self.rooms[1][1][2][1] == entity_

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
        entity_ = self.rooms[1][z][y][x]
        self.world.portal_entity(entity_, 1, 1)
        assert self.rooms[1][z][y][x] != entity_

        x, y, z = self.rooms[0].get_coords(entity_)
        assert self.rooms[0][z][y][x] == entity_
