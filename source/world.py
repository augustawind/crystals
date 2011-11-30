"""world.py - world layout, world rendering, and entity placement"""

import logging

from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup
from pyglet.gl import *

glEnable(GL_TEXTURE_2D)

TILE_SIZE = 24
OFFSET_COLS = 0
OFFSET_ROWS = 2
VIEWPORT_ROWS = 16
VIEWPORT_COLS = 16
VIEWPORT = dict(x1=OFFSET_COLS, x2=OFFSET_COLS + VIEWPORT_COLS,
                y1=OFFSET_ROWS, y2=OFFSET_ROWS + VIEWPORT_ROWS)

class Entity(Sprite):
    """A tangible thing. Populates Rooms."""

    def __init__(self, name, walkable, image, interactable=None):
        super(Entity, self).__init__(image)

        self._name = name
        self._walkable = walkable
        self.interactable = interactable

    @property
    def name(self):
        return self._name

    @property
    def walkable(self):
        return self._walkable

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

        self.entities = {'Character': [], 'Item': [], 'Terrain': []}

        if _map:
            self._map = _map
            self._init_entities()
        else:
            self._map = [[[] for x in width] for y in height]

    def draw(self):
        self.batch.draw()

    # internal methods
    # -------------------------------------------------------------------------

    def _init_entities(self):
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                for entity in self._map[y][x]:
                    self._init_entity(entity, x, y)

    def _init_entity(self, entity, x, y):
        self._update_entity(entity, x, y)
        if str(entity) == 'Character':
            print entity.name, 'tether', self.get_coords(entity)
            entity.set_tether(*self.get_coords(entity))
        self.entities[str(entity)].append(entity)

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
                self.is_walkable(x, y)):
            if str(entity) == 'Character' and not entity.is_in_range(x, y):
                return False
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

class World:
    """A collection of rooms that should be connected to each other by portals.
    """
    
    def __init__(self, rooms, starting_room, hero, ordered_entities):
        self._rooms = rooms
        self._current_room = starting_room
        self.hero = hero

        # add entities to render groups and scale images
        for i in range(len(ordered_entities)):
            for entity in ordered_entities[i]:
                entity.group = OrderedGroup(i)

                # scale image (texture manipulation is to avoid bluriness)
                texture = entity.image.get_texture()
                glBindTexture(GL_TEXTURE_2D, texture.id)
                texture.width = TILE_SIZE
                texture.height = TILE_SIZE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # center camera on the hero
        self._current_room.center_camera(self.hero)

    def draw(self):
        self._current_room.draw()

    # get methods -------------------------------------------------------------
    def get_terrain(self):
        return self._current_room.get_terrain()

    def get_items(self):
        return self._current_room.get_items()

    def get_characters(self):
        return self._current_room.get_characters()

    def is_walkable(self, x, y):
        return self._current_room.is_walkable(x, y)

    def get_portal(self, x, y):
        return self._current_room.get_portal(x, y)

    def get_interactable(self, x, y):
        for entity in self._current_room.get_entities(x, y):
            interactable = entity.interactable
            if interactable:
                return interactable
    
    def get_coords(self, entity):
        return self._current_room.get_coords(entity)

    # adding entities ---------------------------------------------------------
    def add_entity(self, entity, x, y):
        self._current_room.add_entity(entity, x, y)
    
    def insert_entity(self, entity, x, y, z=0):
        self._current_room.add_entity(entity, x, y, z)

    # removing entities -------------------------------------------------------
    def remove_entity(self, entity, x, y):
        self._current_room.remove_entity(entity, x, y)
    
    def pop_entity(self, x, y, z=-1):
        self._current_room.pop_entity(x, y, z)

    # moving entities ---------------------------------------------------------
    def move_entity(self, entity, new_x, new_y):
        if self._current_room.move_entity(entity, new_x, new_y):
            portal = self.get_portal(new_x, new_y)
            if portal and (entity is self.hero):
                self.portal_entity(entity, portal)
            return True
        else:
            return False

    def step_entity(self, entity, x_step, y_step):
        x, y = self.get_coords(entity)
        return self.move_entity(entity, x + x_step, y + y_step)

    def step_hero(self, x_step, y_step):
        if self.step_entity(self.hero, x_step, y_step):
            self._current_room.pan_camera(x_step, y_step)

    def portal_entity(self, entity, portal):
        self._current_room.delete_entity(entity, *portal.coords)
        from_room = self._current_room
        to_room = self._rooms[portal.dest_room]
        to_portal = to_room.get_portal_from_room(from_room)

        self._current_room = to_room
        x, y = to_portal.coords
        self.add_entity(entity, x, y)
        self._current_room.center_camera(entity)
