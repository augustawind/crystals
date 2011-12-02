"""room - rooms and portals, the constituent parts of a world"""

from pyglet.graphics import Batch

from .data import VIEWPORT, VIEWPORT_ROWS, VIEWPORT_COLS, TILE_SIZE

class Portal:
    """A set of coordinates that is connected to a Room. When an Entity is
    moved into the coordinates of a portal, it is transported to the connected
    Room by World."""
    
    def __init__(self, x, y, name, dest):
        self._x = x
        self._y = y
        self._name = name
        self._dest_room, self._dest_portal = dest.split('.')
    
    @property
    def coords(self):
        return self._x, self._y

    @property
    def name(self):
        return self._name

    @property
    def dest_room(self):
        return self._dest_room

    @property
    def dest_portal(self):
        return self._dest_portal

    @property
    def dest(self):
        return self._dest_room, self._dest_portal
        
class Room:
    """A 3-dimensional grid that contains Entities and Portals to other Rooms.
    Populates a World."""

    def __init__(self, name, width, height, _map=[], portals=[]):
        self.name = name
        self.width = width
        self.height = height
        self._portals = portals

        self.batch = Batch()

        self.pan_x = 0
        self.pan_y = 0

        self.entities = {
            'Character': [], 'Item': [], 'Feature': [], 'Terrain': []}

        if _map:
            self._map = _map
            self._init_entities()
        else:
            self._map = [[[] for x in width] for y in height]

    def draw(self):
        self.batch.draw()

    # internal methods
    # -------------------------------------------------------------------------

    def _init_entity(self, entity, x, y):
        self._update_entity(entity, x, y)
        entity.set_tether(*self.get_coords(entity))
        self.entities[str(entity)].append(entity)

    def _init_entities(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                for entity in self._map[y][x]:
                    self._init_entity(entity, x, y)

    def _update_entity(self, entity, x, y):
        x_coord = (x + VIEWPORT['x1'] - self.pan_x) * TILE_SIZE
        y_coord = (y + VIEWPORT['y1'] - self.pan_y) * TILE_SIZE

        entity.set_position(x_coord, y_coord)

        if (VIEWPORT['x1'] <= x - self.pan_x < VIEWPORT['x2'] and
                VIEWPORT['y1'] <= y - self.pan_y < VIEWPORT['y2']):
            entity.batch = self.batch
        else:
            entity.batch = None

    def _update_entities(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                for entity in self._map[y][x]:
                    self._update_entity(entity, x, y)

    def _place_entity(self, entity, x, y):
        if (0 <= x < self.width and 0 <= y < self.height and
                self.is_walkable(x, y) and entity.is_in_range(x, y)):
            self._map[y][x].append(entity)
            return True
        return False

    # public methods
    # -------------------------------------------------------------------------

    @property
    def portals(self):
        return self._portals

    # get methods -------------------------------------------------------------
    def get_map(self):
        return self._map.copy()

    def get_terrain(self):
        return self.entities['Terrain']

    def get_items(self):
        return self.entities['Item']

    def get_characters(self):
        return self.entities['Character']

    def is_walkable(self, x, y):
        return all([e.walkable for e in self._map[y][x]])

    def get_entities(self, x, y):
        return [e for e in self._map[y][x]]

    def get_coords(self, entity):
        x_coord = (entity.x / TILE_SIZE) - VIEWPORT['x1'] + self.pan_x
        y_coord = (entity.y / TILE_SIZE) - VIEWPORT['y1'] + self.pan_y
        return x_coord, y_coord

    def get_portal(self, x, y):
        for portal in self._portals:
            px, py = portal.coords
            if (px == x) and (py == y):
                return portal
    
    def get_portal_from_room(self, room):
        for portal in self._portals:
            if (portal.dest_room == room.name and
                    portal.dest_portal in [p.name for p in room.portals]):
                return portal

    # adding entities ---------------------------------------------------------
    def add_entity(self, entity, x, y):
        if self._place_entity(entity, x, y):
            self._init_entity(entity, x, y)
            return True
        else:
            return False

    def insert_entity(self, entity, x, y, z=0):
        self._map[y][x].insert(z, entity)

    # removing entities -------------------------------------------------------
    def remove_entity(self, entity, x, y):
        self._map[y][x].remove(entity)
     
    def delete_entity(self, entity, x, y):
        self.remove_entity(entity, x, y)
        self.entities[str(entity)].remove(entity)

    def pop_entity(self, x, y, z=-1):
        return self._map[y][x].pop(z)

    # moving entities ---------------------------------------------------------
    def move_entity(self, entity, new_x, new_y):
        if self._place_entity(entity, new_x, new_y):
            old_x, old_y = self.get_coords(entity)
            self.remove_entity(entity, old_x, old_y)
            self._update_entity(entity, new_x, new_y)
            return True
        else:
            return False

    # camera placement --------------------------------------------------------
    def pan_camera(self, x, y):
        self.pan_x += x
        self.pan_y += y
        self._update_entities()

    def center_camera(self, entity):
        x, y = self.get_coords(entity)
        self.pan_x = x - (VIEWPORT_COLS / 2)
        self.pan_y = y - (VIEWPORT_ROWS / 2)
        self._update_entities()
