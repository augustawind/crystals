"""creation and mutation of the game world"""
from pyglet.graphics import OrderedGroup

import entity
from entity import Entity

__all__ = ['Room', 'World', 'entity', 'Entity', 'action']

TILE_SIZE = 24 # Width and height of each tile, in pixels
ORIGIN_X = 10  # X and Y coordinates of the bottom left corner
ORIGIN_Y = 124 # of room display, in pixels


class WorldError(Exception):
    pass


class Room(list):

    def __init__(self, name, batch, grid):
        super(Room, self).__init__(grid)
        self.name = name
        self.batch = batch

    def _update_entity(self, entity, x, y, z):
        """Update the entity's position to reflect (x, y, z). Must only
        be called after at least one call to _focus_entity.
        """
        newx = x * TILE_SIZE + ORIGIN_X
        newy = y * TILE_SIZE + ORIGIN_Y
        entity.set_position(newx, newy)
        entity.group = OrderedGroup(z)

    def _focus_entity(self, entity, x, y, z):
        entity.batch = self.batch
        self._update_entity(entity, x, y, z)

    def focus(self):
        """Focus the room, preparing it for rendering."""
        for y in xrange(len(self)):
            for x in xrange(len(self[y])):
                for z, entity in enumerate(self[y][x]):
                    if entity:
                        self._focus_entity(entity, x, y, z)

    def iswalkable(self, x, y):
        """Return True if, for every layer, (x, y) is in bounds and is
        either None or a walkable entity, else return False.
        """
        if (x < 0 or x >= len(self[0][0])) or (y < 0 or y >= len(self[0])):
            return False
        for e in self[y][x]:
            if e != None and not e.walkable:
                return False
        return True

    def get_coords(self, entity):
        """Return x, y, and z coordinates of the given entity in the room."""
        x = (entity.x - ORIGIN_X) / TILE_SIZE
        y = (entity.y - ORIGIN_Y) / TILE_SIZE
        if entity.group is None:
            z = None
        else:
            z = entity.group.order
        return x, y, z

    def replace_entity(self, entity, x, y, z):
        """Place 'entity' at (x, y, z), replacing an existing entity if
        neccessary.
        """
        self[y][x][z] = entity
        self._focus_entity(entity, x, y, z)


class World(dict):
    """A collection of rooms linked by portals."""

    def __init__(self, rooms, portals, start):
        dict.__init__(self, rooms)

        self._portals_dest2xy = dict.fromkeys(portals, {})
        self._portals_xy2dest = dict.fromkeys(portals, {})
        for from_room, portal in portals.iteritems():
            for dest, xy in portal.iteritems():
                self._portals_dest2xy[from_room][dest] = xy
                self._portals_xy2dest[from_room][xy] = dest

        self._focus = None
        self.set_focus(start)

    @property
    def focus(self):
        return self._focus

    @property
    def portals_dest2xy(self):
        return self._portals_dest2xy

    @property
    def portals_xy2dest(self):
        return self._portals_xy2dest

    def set_focus(self, room_name):
        self._focus = self[room_name]
        self._focus.focus()
    
    def add_entity(self, entity, x, y, z=None, room=''):
        """Add the given entity to the given room at (x, y, z).
        
        If z is None, or out of range, add a layer to the top and put the
        entity there. Otherwise, if no entity exists at [z][y][x], place
        it there, else insert a new layer at z + 1 and place it there.

        If room tests False, add the entity to the focused room.
        """
        room = self[room] if room else self._focus

        if z is None or z >= len(room[y][x]):
            room[y][x].append(None)
            z = -1
        elif room[y][x][z]:
            z += 1
            room[y][x].insert(z, None)
            for i, ent in enumerate(room[y][x][z + 1:]):
                if ent:
                    room.replace_entity(ent, x, y, z + 1 + i)

        room.replace_entity(entity, x, y, z)

    def pop_entity(self, x, y, z, room=''):
        """Remove and return the entity at (x, y, z)."""
        room = self[room] if room else self._focus
        
        entity = room[y][x][z]
        room[y][x][z] = None
        return entity
    
    def step_entity(self, entity, xstep, ystep):
        """Move entity from its current position by (xstep, ystep),
        changing the direction of the entity to reflect the direction of
        the attempted move. 
        
        Return True if the move was successful, else False.
        """
        entity.facing = (xstep / abs(xstep) if xstep else 0,
                      ystep / abs(ystep) if ystep else 0)

        x, y, z = self._focus.get_coords(entity)
        newx = x + xstep
        newy = y + ystep
        if not self._focus.iswalkable(newx, newy):
            return False

        self.pop_entity(x, y, z)
        self.add_entity(entity, newx, newy, z)
        return True

    def portal_entity(self, entity, x, y):
        """If a portal exists at (x, y), transfer entity from its
        current room to the destination room of the portal.
        """
        destname = self.portals_xy2dest[self._focus.name][(x, y)]
        z = self._focus.get_coords(entity)[2]
        self.pop_entity(x, y, z)
        x, y = self.portals_dest2xy[destname][self._focus.name]
        self.add_entity(entity, x, y, z, destname)
