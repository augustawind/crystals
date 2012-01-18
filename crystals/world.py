"""creation and mutation of the game world"""
from pyglet.graphics import OrderedGroup

TILE_SIZE = 24

class WorldError(Exception):
    pass


class Room(list):

    def __init__(self, name, batch, layers):
        super(Room, self).__init__(layers)
        self.name = name
        self.batch = batch
        self.groups = [OrderedGroup(z) for z in range(len(self))]

    def _update_entity(self, entity, x, y, z):
        entity.batch = self.batch
        entity.group = self.groups[z]
        entity.set_position(x * TILE_SIZE, y * TILE_SIZE)

    def replace_entity(self, entity, x, y, z):
        """Place 'entity' at (x, y, z), replacing an existing entity if
        neccesary."""
        self[z][y][x] = entity
        self._update_entity(entity, x, y, z)

    def add_entity(self, entity, x, y, z):
        """Attempt to place 'entity' at (x, y, z), but raise a
        WorldError if an entity already exists there."""
        if self[z][y][x] is not None:
            raise WorldError(
                'Entity already exists in room {}[{}][{}][{}]'.format(
                self.name, z, y, x))
        self.replace_entity(entity, x, y, z)

    def focus(self):
        """Focus the room, preparing it for rendering."""
        for z in range(len(self)):
            for y in range(len(self[z])):
                for x in range(len(self[z][y])):
                    entity = self[z][y][x]
                    if entity is not None:
                        self._update_entity(entity, x, y, z)


class World(dict):

    def __init__(self, rooms, current_room):
        dict.__init__(self, rooms)
        self.focus = None
        self.set_focus(current_room)

    def set_focus(self, room_name):
        self.focus = self[room_name]
        self.focus.focus()
