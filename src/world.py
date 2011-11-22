"""world - methods for world generation and manipulation"""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch

TILE_WIDTH = 24
TILE_HEIGHT = 24

class Entity(Sprite):
    """A tangible thing. Populates Rooms."""

    def __init__(self, name, walkable, image):
        super(Entity, self).__init__(image)

        self.name = name
        self.walkable = walkable

    def get_name(self):
        return self.name

    def is_walkable(self):
        return self.walkable

class Portal:
    """A set of coordinates that is connected to a Room. When an Entity is
    moved into the coordinates of a portal, it is transported to the connected
    Room by World."""
    
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room
    
    def get_coords(self):
        return self.x, self.y
    
    def get_room(self):
        return self.room
        
class Room:
    """A 3-dimensional grid that contains Entities and Portals to other Rooms.
    Populates a World."""

    def __init__(self, name, width, height, _map=[], portals=[]):
        self.width = width
        self.height = height
        self.portals = portals

        self.batch = Batch()

        if _map:
            self._map = _map
            self._init_entities()
        else:
            self._map = [[[] for x in width] for y in height]

    def _init_entities(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                for entity in self._map[y][x]:
                    self._init_entity(entity, x, y)

    def _init_entity(self, entity, x, y):
        entity.batch = self.batch
        self._update_entity(entity, x, y)

    def _update_entity(self, entity, x, y):
        entity.set_position(x * TILE_WIDTH, y * TILE_HEIGHT)

    def get_coords(self, entity):
        x, y = entity.position
        return x / TILE_WIDTH, y / TILE_HEIGHT

    def is_walkable(self, x, y):
        return all([e.is_walkable() for e in self._map[y][x]])

    def _place_entity(self, entity, x, y):
        if (self.is_walkable(x, y) and
                0 <= x < self.width and
                0 <= y < self.height):
            self._map[y][x].append(entity)
            return True
        else:
            return False

    def add_entity(self, entity, x, y):
        if self._place_entity(entity, x, y):
            self._init_entity(entity, x, y)
            return True
        else:
            return False

    def insert_entity(self, entity, x, y, z=0):
        self._map[y][x].insert(z, entity)

    def remove_entity(self, entity, x, y):
        self._map[y][x].remove(entity)

    def delete_entity(self, entity):
        self.remove_entity(entity)
        entity.delete()

    def pop_entity(self, x, y, z=-1):
        return self._map[y][x].pop(z)

    def move_entity(self, entity, new_x, new_y):
        x, y = self.get_coords(entity)
        if self._place_entity(entity, new_x, new_y):
            self._update_entity(entity, new_x, new_y)
            self.remove_entity(entity, x, y)
            return True
        return False

    def get_portal(self, x, y):
        for portal in self.portals:
            if portal.get_coords() is (x, y): 
                return portal
    
    def get_portal_from_room(self, room):
        for portal in self.portals:
            if portal.get_room() is room:
                return portal
    
    def draw(self):
        self.batch.draw()

class World:
    """A collection of rooms that should be connected to each other by portals.
    """
    
    def __init__(self, rooms, initial_room, hero):
        self.rooms = rooms
        self.current_room = initial_room
        self.hero = hero

    def get_hero(self):
        return self.hero
    
    def is_walkable(self, x, y):
        return self.current_room.is_walkable(x, y)
    
    def get_coords(self, entity):
        return self.current_room.get_coords(entity)
    
    def add_entity(self, entity, x, y):
        self.current_room.add_entity(entity, x, y)
    
    def insert_entity(self, entity, x, y, z=0):
        self.current_room.add_entity(entity, x, y, z)
    
    def remove_entity(self, entity, x, y):
        self.current_room.remove_entity(entity, x, y)
    
    def pop_entity(self, x, y, z=-1):
        self.current_room.pop_entity(x, y, z)
    
    def move_entity(self, entity, new_x, new_y):
        if self.current_room.move_entity(entity, new_x, new_y):
            portal = self.current_room.get_portal(new_x, new_y)
            if portal:
                old_room = self.current_room
                self.current_room = portal.get_room()
                receiving_portal = self.current_room.get_portal_from_room(old_room)
                new_x, new_y = receiving_portal.get_coords()
                self.current_room.add_entity(entity, new_x, new_y)
            return True
        return False

    def step_entity(self, entity, x_step, y_step):
        x, y = self.get_coords(entity)
        self.move_entity(entity, x + x_step, y + y_step)
    
    def draw(self):
        self.current_room.draw()
                
