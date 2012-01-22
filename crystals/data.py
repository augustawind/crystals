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
        """Load all images in res_path/archetype.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'goblin.png' --> 'goblin'.
        """
        path = os.path.join(path, archetype)
        for filename in os.listdir(path):
            key = os.path.splitext(filename)[0]
            image = pyglet.image.load(os.path.join(path, filename))
            self[key] = image


class WorldLoader(object):
    """Loads the game world."""

    def __init__(self, res_path=RES_PATH):
        # Ensure data and resource paths are valid

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
        self.mapkey = self.atlas.mapkey # Default map key

        self.player = None

        glEnable(GL_TEXTURE_2D) # Needed for smooth image scaling

    def __del__(self):
        """Revert GL changes."""
        glDisable(GL_TEXTURE_2D)

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

    def _scale_image(self, image):
        """Scale `image` to TILE_SIZE x TILE_SIZE."""
        texture = image.get_texture()
        glBindTexture(GL_TEXTURE_2D, texture.id)
        texture.width = TILE_SIZE
        texture.height = TILE_SIZE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def load_entity(self, kwargs):
        """Return an entity instance, given its parameters."""
        self._scale_image(kwargs['image'])
        return entity.Entity(**kwargs)

    def load_general_entity_args(self, room_name, archetype):
        """Return a dict of archetype-independent argument dicts for entities,
        given a room name and archetype.
        
        The returned dict maps argument tuples to unique names
        generated from the config file.
        """
        if hasattr(self.configs[archetype], room_name):
            config = getattr(self.configs[archetype], room_name).entities
            defaults = self.defaults[archetype]
        else:
            config = {}

        entity_args = {}
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
                entity_args[key] = params

        return entity_args
    
    def load_terrain_args(self, room_name):
        """Return argument dicts for terrain entities, given a room name."""
        return self.load_general_entity_args(room_name, 'terrain')

    def load_feature_args(self, room_name):
        """Return argument dicts for feature entities, given a room name."""
        return self.load_general_entity_args(room_name, 'feature')

    def load_item_args(self, room_name):
        """Return argument dicts for item entities, given a room name."""
        return self.load_general_entity_args(room_name, 'item')
    
    def load_character_args(self, room_name):
        """Return argument dicts for character entities, given a room name."""
        archetype = 'character'
        args = self.load_general_entity_args(room_name, archetype)

        # Player
        args['player'] = self.configs[archetype].player.copy()
        args['player']['archetype'] = archetype
        image_name = args['player']['image']
        args['player']['image'] = self.images[
            archetype][image_name]

        # All characters 
        for key in args:
            args[key]['walkable'] = False

        return args

    def load_entity_args(self, room_name):
        """Return argument dicts for all entities, given a room name."""
        args = {}
        for argsloader in (self.load_terrain_args, self.load_feature_args,
                           self.load_item_args, self.load_character_args):
            entity_args = argsloader(room_name)
            args.update(entity_args)
        return args

    def load_room(self, room_name):
        """Load and return a Room instance, given a room name."""
        entity_args = self.load_entity_args(room_name)
        atlas = getattr(self.atlas, room_name)
        mapkey = self.mapkey.copy()
        mapkey.update(atlas.mapkey)

        # Build the room
        layers = []
        for layer in atlas.maps:
            layers.append([])
            for row in reversed(layer.strip().split('\n')):
                layers[-1].append([])
                for symbol in row.strip():
                    # Place None if IGNORE_SYMBOL is encountered
                    if symbol == IGNORE_SYMBOL:
                        entity_ = None
                    # Place the player if PLAYER_SYMBOL is encountered
                    elif symbol == PLAYER_SYMBOL:
                        entity_ = self.load_entity(entity_args['player'])
                        self.player = entity_
                    else:
                        key = mapkey[symbol] 
                        kwargs = entity_args[key]
                        entity_ = self.load_entity(entity_args[key])
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
