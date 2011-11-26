"""world - methods for world generation and manipulation"""
import logging

from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup

TILE_WIDTH = 24
TILE_HEIGHT = 24

class Entity(Sprite):
    """A tangible thing. Populates Rooms."""

    def __init__(self, name, walkable, image, interactable=None):
        super(Entity, self).__init__(image)

        self.name = name
        self.walkable = walkable
        self.interactable = interactable

    def get_name(self):
        return self.name

    def is_walkable(self):
        return self.walkable

    def get_interactable(self):
        return self.interactable

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
        self.name = name
        self.width = width
        self.height = height
        self.portals = portals

        self.batch = Batch()

        self.entities = {'Character': [], 'Item': [], 'Terrain': []}

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
        logging.debug('{}._init_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))

        entity.batch = self.batch
        self._update_entity(entity, x, y)
        self.entities[str(entity)].append(entity)
        
        logging.debug('{}.entities[{}][-1] is now {}'.format(
            self.name, str(entity), entity.get_name()))

    def _update_entity(self, entity, x, y):
        logging.debug('{}._update_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))

        entity.set_position(x * TILE_WIDTH, y * TILE_HEIGHT)

    def get_entities(self, x, y):
        return [e for e in self._map[y][x]]

    def get_terrain(self):
        return self.entities['Terrain']

    def get_items(self):
        return self.entities['Item']

    def get_characters(self):
        return self.entities['Character']

    def get_coords(self, entity):
        x, y = entity.position
        return x / TILE_WIDTH, y / TILE_HEIGHT

    def is_walkable(self, x, y):
        return all([e.is_walkable() for e in self._map[y][x]])

    def add_portals(self, *portals):
        self.portals.extend(portals)

    def _place_entity(self, entity, x, y):
        logging.debug('{}._place_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))

        if (0 <= x < self.width and 0 <= y < self.height and
                self.is_walkable(x, y)):
            logging.debug('{}._place_entity ==> in bounds and walkable'.format(
                self.name))
            self._map[y][x].append(entity)
            logging.debug(
                '{}._place_entity ==> _map[{}][{}][-1] is now {}'.format(
                    self.name, y, x, self._map[y][x][-1]))
            return True
        else:
            logging.debug(
                '{}._place_entity ==> out of bounds or not walkable'.format(
                    self.name))
            return False

    def add_entity(self, entity, x, y):
        logging.debug('{}.add_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))

        if self._place_entity(entity, x, y):
            self._init_entity(entity, x, y)
            logging.debug('{}.add_entity ==> entity added'.format(self.name))
            return True
        else:
            logging.debug('{}.add_entity ==> entity couldnt be added'.format(
                self.name))
            return False

    def insert_entity(self, entity, x, y, z=0):
        self._map[y][x].insert(z, entity)

    def remove_entity(self, entity, x, y):
        logging.debug('{}.remove_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))
        
        self._map[y][x].remove(entity)
     
    def delete_entity(self, entity, x, y):
        logging.debug('{}.delete_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), x, y))

        self.remove_entity(entity, x, y)
        self.entities[str(entity)].remove(entity)
        
        logging.debug('{} in {}.entities is {}'.format(
            entity.get_name(), self.name, entity in self.entities))

    def pop_entity(self, x, y, z=-1):
        return self._map[y][x].pop(z)

    def move_entity(self, entity, new_x, new_y):
        logging.debug('{}.move_entity({}, x={}, y={})'.format(
            self.name, entity.get_name(), new_x, new_y)) 
        
        if self._place_entity(entity, new_x, new_y):
            old_x, old_y = self.get_coords(entity)
            self.remove_entity(entity, old_x, old_y)
            self._update_entity(entity, new_x, new_y)
            return True
        else:
            return False

    def get_portal(self, x, y):
        for portal in self.portals:
            px, py = portal.get_coords()
            if (px == x) and (py == y):
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
    
    def __init__(self, rooms, starting_room, hero, ordered_entities):
        self.rooms = rooms
        self.current_room = starting_room
        self.hero = hero

        self.render_groups = []
        for i in range(len(ordered_entities)):
            self.render_groups.append(OrderedGroup(i))
            for entity in ordered_entities[i]:
                entity.group = self.render_groups[-1]

    def get_hero(self):
        return self.hero

    def get_terrain(self):
        return self.current_room.get_terrain()

    def get_items(self):
        return self.current_room.get_items()

    def get_characters(self):
        return self.current_room.get_characters()
    
    def is_walkable(self, x, y):
        return self.current_room.is_walkable(x, y)

    def get_portal(self, x, y):
        return self.current_room.get_portal(x, y)

    def get_interactable(self, x, y):
        for entity in self.current_room.get_entities(x, y):
            interactable = entity.get_interactable()
            if interactable:
                return interactable
    
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
            portal = self.get_portal(new_x, new_y)
            if portal:
                self.portal_entity(entity, portal)
            return True
        else:
            return False

    def step_entity(self, entity, x_step, y_step):
        x, y = self.get_coords(entity)
        return self.move_entity(entity, x + x_step, y + y_step)

    def portal_entity(self, entity, portal):
        logging.debug('{}.portal_entity({}, {})'.format(
            'World', entity.get_name(), portal.get_room().name))
        
        self.current_room.delete_entity(entity, *portal.get_coords())
        old_room = self.current_room
        self.current_room = portal.get_room()
        recieving_portal = self.current_room.get_portal_from_room(
            old_room)
        x, y = recieving_portal.get_coords()
        self.add_entity(entity, x, y)
    
    def draw(self):
        self.current_room.draw()
