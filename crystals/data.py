"""tools for loading variable game data and resources"""
import os
import sys
import pyglet
from pyglet.gl import *

from crystals import entity
from crystals.world import TILE_SIZE
from crystals.world import Room
from crystals.world import World

RES_PATH = os.path.join('crystals', 'res') # default path to game resources
ARCHETYPES = ('terrain', 'feature', 'item', 'character') # entity categories
PLAYER_SYMBOL = '@' # char that represents the player
IGNORE_SYMBOL = '.' # char to ignore when reading maps

# Parameter names for all entities
ENTITY_PARAMS = ('name', 'archetype', 'walkable', 'image')

class ResourceError(Exception):
    """Exception class for errors in loading game resources."""
    pass


class ImageDict(dict):
    """Loads game images."""

    def __init__(self, archetype, path=os.path.join(RES_PATH, 'image')):
        """Load all images in res_path/archetype, and scale them to TILE_SIZE.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'goblin.png' --> 'goblin'.
        """
        glEnable(GL_TEXTURE_2D)

        path = os.path.join(path, archetype)
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

    def __init__(self, res_path=RES_PATH):
        # Ensure data and resource paths are valid
        self._validate_res_path(res_path)

        # Load images
        image_path = os.path.join(res_path, 'image')
        self.images = dict((a, ImageDict(a, image_path)) for a in ARCHETYPES)
        
        # Load world data
        world_path = os.path.join(res_path, 'world')
        sys.path.insert(0, world_path) # Add world directory to PYTHONPATH
        self.configs = {}
        self.defaults = {}
        for archetype in ARCHETYPES:
            self.configs[archetype] =  __import__(archetype)
            if hasattr(self.configs[archetype], 'entities'):
                self.defaults[archetype] = self.configs[archetype].entities

        self.atlas = __import__('atlas')
        self.symbols = self.atlas.symbols # Default symbols

        self.player = None

    def _validate_res_path(self, res_path):
        """Raise a ResourceError if res_path is invalid."""
        image_path = os.path.join(res_path, 'image')
        if not os.path.exists(image_path):
            raise ResourceError("Resource path must contain " +
                                 "subdirectory 'image'")
        world_path = os.path.join(res_path, 'world')
        if not os.path.exists(world_path):
            raise ResourceError("Resource path must contain subdirectory " +
                                "'world'")
        for archetype in ARCHETYPES:
            if not os.path.exists(os.path.join(image_path, archetype)):
                raise ResourceError("Image path must contain subdirectory '" +
                                    archetype + "'")
            if not os.path.exists(os.path.join(world_path, archetype + '.py')):
                raise ResourceError("World path must contain module '" +
                                    archetype + "'")
        if not os.path.exists(os.path.join(world_path, 'atlas.py')):
            raise ResourceError("World path must contain module 'atlas'")

    def load_archetype_args(self, room_name, archetype):
        """Load the arguments for each entity for a given room and archetype.
        
        Return a dict object mapping argument tuples to unique names
        generated from the config file. If no data is found, return an
        empty dict.
        """
        if hasattr(self.configs[archetype], room_name):
            config = getattr(self.configs[archetype], room_name).entities
            defaults = self.defaults[archetype]
        else:
            config = {}

        archetype_args = {}
        for clsname, clscfg in config.iteritems():
            # Load entity class parameters
            clsparams = {}
            clsdefaults = defaults.get(clsname, {})
            if 'params' in clsdefaults:
                clsparams.update(clsdefaults['params']) # Add defaults
            clsparams.update(clscfg.get('params', {})) # Add room-specifics

            for specname, speccfg in clscfg.iteritems():
                if specname == 'params':
                    continue
                # Load entity specific parameters
                params = clsparams.copy()
                specdefaults = clsdefaults.get(specname, {})
                params.update(specdefaults) # Add defaults
                params.update(speccfg) # Add room-specifics

                params['archetype'] = archetype
                if 'variant' in params:
                    # Combine image and variant params to get the image name
                    params['image'] += '-' + params.pop('variant')
                # Replace the image name with the actual image object
                params['image'] = self.images[archetype][params['image']]
                
                # Map an Entity instance to a unique identifier
                key = clsname + '-' + specname
                archetype_args[key] = params

        if archetype == 'character':
            archetype_args['player'] = self.configs[archetype].player.copy()
            archetype_args['player']['archetype'] = archetype
            image_name = archetype_args['player']['image']
            archetype_args['player']['image'] = self.images[
                archetype][image_name]

            for key in archetype_args.iterkeys():
                archetype_args[key]['walkable'] = False

        return archetype_args

    def load_entity_args(self, room_name):
        """Load the arguments for each entity for a given room for
        every archetype.

        Return a dict object mapping argument tuples to unique names
        generated from the config file. If no data is found, raise an
        exception.
        """
        entity_args = {}
        for archetype in ARCHETYPES:
            archetype_args = self.load_archetype_args(room_name, archetype)
            entity_args.update(archetype_args)

        return entity_args

    def load_room(self, room_name):
        """Load and return a Room instance, given a room name."""
        entity_args = self.load_entity_args(room_name)
        atlas = getattr(self.atlas, room_name)
        symbols = self.symbols.copy()
        symbols.update(atlas.symbols)

        # Build the room
        layers = []
        for layer in atlas.maps:
            layers.append([])
            for row in layer.strip().split('\n'):
                layers[-1].append([])
                for symbol in row.strip():
                    # Place None if IGNORE_SYMBOL is encountered
                    if symbol == IGNORE_SYMBOL:
                        entity_ = None
                    # Place the player if PLAYER_SYMBOL is encountered
                    elif symbol == PLAYER_SYMBOL:
                        kwargs = entity_args['player']
                        entity_ = entity.Entity(**kwargs)
                        self.player = entity_
                    else:
                        key = symbols[symbol] 
                        kwargs = entity_args[key]
                        entity_ = entity.Entity(**kwargs)
                    layers[-1][-1].append(entity_)

        # The room gets a unique batch
        return Room(room_name, pyglet.graphics.Batch(), layers)

    def load_world(self):
        """Load and return a World instance and the player entity instance."""
        rooms = dict((room_name, self.load_room(room_name))
                 for room_name in self.atlas.rooms)
        starting_room = self.atlas.starting_room
        world = World(rooms, starting_room)
        
        return world, self.player
