"""creation and mutation of the game world"""
from pyglet.graphics import OrderedGroup

TILE_SIZE = 24 # Width and height of each tile, in pixels
ORIGIN_X = 10  # X and Y coordinates of the bottom left corner
ORIGIN_Y = 124 # of room display, in pixels

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
        newx = x * TILE_SIZE + ORIGIN_X
        newy = y * TILE_SIZE + ORIGIN_Y
        entity.set_position(newx, newy)

    def iswalkable(self, x, y):
        """Return True if, for every layer, (x, y) is in bounds and is
        either None or a walkable entity, else return False.
        """
        if (x < 0 or x >= len(self[0][0])) or (y < 0 or y >= len(self[0])):
            return False
        for layer in self:
            e = layer[y][x]
            if e != None and not e.walkable:
                return False
        return True

    def focus(self):
        """Focus the room, preparing it for rendering."""
        for z in range(len(self)):
            for y in range(len(self[z])):
                for x in range(len(self[z][y])):
                    entity = self[z][y][x]
                    if entity is not None:
                        self._update_entity(entity, x, y, z)

    def get_coords(self, entity):
        x = (entity.x - ORIGIN_X) / TILE_SIZE
        y = (entity.y - ORIGIN_Y) / TILE_SIZE
        if entity.group is None:
            z = None
        else:
            z = entity.group.order
        return x, y, z

    def add_layer(self, z=None):
        """If z is None or too large, append a blank layer at the top.
        If z is an integer, insert a blank layer at z. 
        """
        layer = [[None for x in range(len(self[0][0]))]
                 for y in range(len(self[0]))]
        if z is None or z >= len(self):
            self.append(layer)
            self.groups.append(OrderedGroup(len(self.groups)))
        else:
            self.insert(z, layer)
            self.groups.insert(z, OrderedGroup(z))
            for group in self.groups[z + 1:]:
                group.order += 1

    def replace_entity(self, entity, x, y, z):
        """Place 'entity' at (x, y, z), replacing an existing entity if
        neccesary.
        """
        self[z][y][x] = entity
        self._update_entity(entity, x, y, z)

    def add_entity(self, entity, x, y, z):
        """Attempt to place 'entity' at (x, y, z), but raise a
        WorldError if an entity already exists there.
        """
        if self[z][y][x] is not None:
            raise WorldError(
                'Entity already exists in room {}[{}][{}][{}]'.format(
                self.name, z, y, x))
        self.replace_entity(entity, x, y, z)


class World(dict):

    def __init__(self, rooms, current_room):
        dict.__init__(self, rooms)
        self.focus = None
        self.set_focus(current_room)

    def set_focus(self, room_name):
        self.focus = self[room_name]
        self.focus.focus()
    
    def add_entity(self, entity, x, y, z=None):
        """Add an entity at [z][y][x] in the focused room.
        
        If z is None, add a layer to the top and put the
        entity there. Otherwise, if no entity exists at [z][y][x],
        place it there, else insert a new layer at z + 1 and place it there.
        """
        if z is None:
            z = -1
            self.focus.add_layer()
            self.focus.replace_entity(entity, x, y, -1)
            return
        try:
            self.focus.add_entity(entity, x, y, z)
        except WorldError:
            z += 1
            self.focus.add_layer(z)
            self.focus.replace_entity(entity, x, y, z)

    def pop_entity(self, x, y, z):
        entity = self.focus[z][y][x]
        self.focus[z][y][x] = None
        return entity
    
    def step_entity(self, entity, xstep, ystep):
        x, y, z = self.focus.get_coords(entity)
        newx = x + xstep
        newy = y + ystep
        if not self.focus.iswalkable(newx, newy):
            return
        self.pop_entity(x, y, z)
        self.add_entity(entity, newx, newy, z)


