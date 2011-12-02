"""world - world layout, world rendering, and entity placement"""

from pyglet.graphics import OrderedGroup

from .data import *
from . import room

__all__ = ['TILE_SIZE', 'VIEWPORT_ROWS', 'VIEWPORT_COLS', 'OFFSET_ROWS',
    'OFFSET_COLS', 'VIEWPORT', 'room', 'World']

class World:
    """A collection of rooms that should be connected to each other by portals.
    """
    
    def __init__(self, rooms, starting_room, hero):
        self._rooms = rooms
        self._current_room = starting_room
        self.hero = hero

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

    def get_portal(self, x, y):
        return self._current_room.get_portal(x, y)

    def get_interactions(self, x, y):
        for entity in self._current_room.get_entities(x, y):
            if entity.interactable:
                return entity.iter_interactions()
    
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
        if str(entity) == 'Character':
            entity.set_direction(x_step, y_step)

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
