"""tools for loading game resources"""
import os
import sys

import pyglet
from pyglet.gl import *

from crystals import entity
from crystals.world import TILE_SIZE
from crystals.world import Room
from crystals.world import World

__all__ = ['world']

RES_PATH = os.path.join('crystals', 'res') # default path to game resources
DATA_PATH = os.path.join('crystals', 'data') # default path to game data
ARCHETYPES = ('terrain', 'feature', 'item', 'character') # entity categories

class ImageDict(dict):
    """Loads game images."""

    def __init__(self, img_dir, res_path=RES_PATH):
        """Load all images in RES_PATH/img_dir, and scale them to TILE_SIZE.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'goblin.png' --> 'goblin'.
        """
        glEnable(GL_TEXTURE_2D)

        path = os.path.join(res_path, 'image', img_dir)
        for filename in os.listdir(path):
            key = filename.rsplit('.', 1)[0]
            image = pyglet.image.load(os.path.join(path, filename))

            texture = image.get_texture()
            glBindTexture(GL_TEXTURE_2D, texture.id)
            texture.width = TILE_SIZE
            texture.height = TILE_SIZE

            self[key] = image

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glDisable(GL_TEXTURE_2D)


class WorldLoader(object):
    """Loads the game world."""

    def __init__(self, data_path=DATA_PATH, res_path=RES_PATH):
        self.res_path = res_path
        self.world_path = os.path.join(self.res_path, 'world')
        self.room_path = os.path.join(self.world_path, 'rooms')
        self.rooms = {}
        self.images = dict.fromkeys(ARCHETYPES)
        self.ignore_char = '.' # char to ignore when reading room maps

        # add data_path to PYTHON_PATH and import world data
        sys.path.insert(0, os.path.join(data_path, 'world'))
        self.config = dict((a, __import__(a)) for a in ARCHETYPES)
        self.config['maps'] = __import__('maps')

    def load_images(self, archetype):
        """Load all images for the given archetype."""
        self.images[archetype] = ImageDict(archetype, self.res_path)

    def load_archetype_args(self, room_name, archetype):
        """Load the arguments for each entity for a given room and archetype.
        
        Return a dict object mapping the entity symbols to argument
        tuples. If no data is found, return an empty dict.
        """
        images = ImageDict(archetype)
        if not hasattr(self.config[archetype], room_name):
            return {}
        # load config object from DATA_PATH/world
        config = getattr(self.config[archetype], room_name)

        archetype_args = {}
        for category_name, category in config.entities.iteritems():
            default_params = config.defaults[category_name].copy()
            for entity_name, params in category.iteritems():
                params = params.copy() # Leave module data intact
                params['archetype'] = archetype
                # If name is not given in any params, generate one
                if 'name' not in params and 'name' not in default_params:
                    params['name'] = category_name + '-' + entity_name
                # Replace missing entries from params with entries from
                # default_params
                for key in ('name', 'walkable', 'image', 'color', 'symbol'):
                    if key not in params:
                        params[key] = default_params[key]
                # Combine image and color params to get the image name
                params['image'] += '-' + params.pop('color')
                # Replace the image name with the actual image object
                params['image'] = images[params['image']]
                
                # Map the symbol to a corresponding Entity instance
                symbol = params.pop('symbol')
                archetype_args[symbol] = params

        return archetype_args

    def load_entity_args(self, room_name):
        """Load the arguments for each entity for a given room.

        Return a dict object mapping the entity symbols to argument
        tuples. If no data is found, return an empty dict.
        """
        entity_args = {}
        for atype in ARCHETYPES:
            archetype_args = self.load_archetype_args(room_name, atype)
            entity_args.update(archetype_args)

        return entity_args

    def load_room(self, room_name):
        """Load and return a Room instance, given a room name."""
        entity_args = self.load_entity_args(room_name)
        layers = getattr(self.config['maps'], room_name)
        grid = []
        for layer in layers:
            grid.append([])
            for row in layer.strip().split('\n'):
                grid[-1].append([])
                for symbol in row.strip():
                    if symbol == '.':
                        # Append None when a '.' (period) is encountered
                        grid[-1][-1].append(None)
                    else:
                        entity_ = entity.Entity(**entity_args[symbol])
                        grid[-1][-1].append(entity_)

        # Each room gets a separate batch
        return Room(room_name, pyglet.graphics.Batch(), grid)

    def load_world(self):
        """Load and return a World instance."""
        rooms = dict((room_name, self.load_room(room_name))
                 for room_name in self.config['maps'].rooms)
        starting_room = self.config['maps'].starting_room
        world = World(rooms, starting_room)
        
        return world
