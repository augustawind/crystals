"""tools for loading variable game data and resources"""
import os
import sys
import pyglet
from pyglet.gl import *

from crystals import entity
from crystals.world import TILE_SIZE
from crystals.world import Portal
from crystals.world import Room
from crystals.world import World

RES_PATH = os.path.join('crystals', 'res') # default path to game resources
ARCHETYPES = ('terrain', 'feature', 'item', 'character') # entity categories
PLAYER_SYMBOL = '@' # char that represents the player
IGNORE_SYMBOL = '.' # char to ignore when reading maps
# Parameter names for all entities
ENTITY_PARAMS = ('name', 'archetype', 'walkable', 'image')

glEnable(GL_TEXTURE_2D)

class ResourceError(Exception):
    """Exception class for errors in loading game resources."""


class InsertPath(object):
    """Context manager that inserts a given path into sys.path, then
    removes it."""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.path.remove(self.path)


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


def _validate_res_path(res_path):
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


def _scale_image(image):
    """Scale `image` to TILE_SIZE x TILE_SIZE."""
    texture = image.get_texture()
    glBindTexture(GL_TEXTURE_2D, texture.id)
    texture.width = TILE_SIZE
    texture.height = TILE_SIZE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def _load_entity(kwargs):
    """Return an entity instance, given its parameters."""
    _scale_image(kwargs['image'])
    return entity.Entity(**kwargs)


def _load_global_entity_args(room_name, archetype, config, defaults,
                             imagedict):
    """Return a dict of archetype-independent Entity keyword arguments
    mapped to their entities's  id names, respectively, given a room
    name, an archetype, a dict of entity config objects for the
    archetype, a dict of entity defaults dicts for the archetype, and an
    ImageDict of the given archetype.
    """
    try:
        config = getattr(config, room_name).entities
    except AttributeError:
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
            specparams = clsparams.copy()
            specdefaults = clsdefaults.get(specname, {})
            specparams.update(specdefaults) # Add defaults
            specparams.update(speccfg) # Add room-specifics

            specparams['archetype'] = archetype
            if 'variant' in specparams:
                # Combine image and variant specparams to get the image name
                specparams['image'] += '-' + specparams.pop('variant')
            # Replace the image name with the actual image object
            specparams['image'] = imagedict[specparams['image']]
            
            # Map an Entity instance to a unique identifier
            key = clsname + '-' + specname
            entity_args[key] = specparams

    return entity_args


def _load_terrain_args(room_name, config, defaults, imagedict):
    """Return keyword argument for all terrain entities for the given room.
    
    See `_load_global_entity_args`.
    """
    archetype = 'terrain'
    return _load_global_entity_args(room_name, 'terrain', config, defaults,
                                    imagedict)

def _load_feature_args(room_name, config, defaults, imagedict):
    """Return keyword argument for all feature entities for the given room.
    
    See `_load_global_entity_args`.
    """
    archetype = 'feature'
    return _load_global_entity_args(room_name, 'feature', config, defaults,
                                    imagedict)

def _load_item_args(room_name, config, defaults, imagedict):
    """Return keyword argument for all item entities for the given room.
    
    See `_load_global_entity_args`.
    """
    archetype = 'item'
    return _load_global_entity_args(room_name, 'item', config, defaults,
                                    imagedict)

def _load_character_args(room_name, config, defaults, imagedict):
    """Return keyword argument for all character entities for the given room.
    
    See `_load_global_entity_args`.
    """
    archetype = 'character'
    args = _load_global_entity_args(room_name, archetype, config, defaults,
                                    imagedict)
    for key in args:
        args[key]['walkable'] = False

    return args


def _load_entity_args(room_name, configs, defaults, image_path):
    """Return a dict of Entity keyword arguments mapped to its Entity's
    id name, given a room name, a dict of entity config objects for each
    archetype, a dict of entity defaults dicts for each archetype,
    and an image path.
    """
    args = {}
    for archetype in ARCHETYPES:
        argsloader = getattr(sys.modules[__name__],
                             '_load_{}_args'.format(archetype))
        imagedict = ImageDict(archetype, image_path)
        entity_args = argsloader(room_name, configs.get(archetype, {}),
                                 defaults.get(archetype, {}), imagedict)
        args.update(entity_args)
    return args


def _load_portals(from_room, portalmap, portalkey, rooms):
    """Return a list of portals, given a symbolic map string `portalmap`,
    indicating the portals' coordinates in the room, and a dict `portalkey`
    mapping the destination rooms of each portal to the map symbols.
    """
    maplist = list(reversed(portalmap.strip().split('\n')))
    portals = []
    for y in range(len(maplist)):
        row = maplist[y]
        for x in range(len(row)):
            symbol = row[x]
            if symbol in portalkey:
                to_room = rooms[portalkey[symbol]]
                portal = Portal(x, y, from_room, to_room)
                portals.append(portal)

    return portals


def _load_room(atlas, default_mapkey, configs, defaults, player, image_path):
    """Return a Room instance, given an atlas object, a dict of entity
    config objects for each archetype, a dict of entity defaults dicts
    for each archetype, an image path, and a player Entity instance.
    """
    room_name = atlas.__name__
    entity_args = _load_entity_args(room_name, configs, defaults, image_path)

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
                    entity_ = player
                else:
                    # If symbol is not found in room.mapkey, check
                    # default_mapkey
                    if symbol in atlas.mapkey:
                        key = atlas.mapkey[symbol]
                    else:
                        key = default_mapkey[symbol]

                    kwargs = entity_args[key]
                    entity_ = _load_entity(entity_args[key])
                layers[-1][-1].append(entity_)

    # The room gets a unique batch
    return Room(room_name, pyglet.graphics.Batch(), layers)


def _load_player(config, image_path):
    """Load and return an instance of the player character entity,
    given a dict of parameters and an image path.
    """
    kwargs = config.copy()
    kwargs['archetype'] = 'character'
    kwargs['walkable'] = False
    image_name = kwargs['image']
    kwargs['image'] = ImageDict('character', image_path)[image_name]

    return _load_entity(kwargs)


def _load_world(configs, defaults, atlas, player, image_path):
    """Load and return a World instance."""
    # Load rooms
    rooms = {}
    for room_name in atlas.rooms:
        room_atlas = getattr(atlas, room_name)
        default_mapkey = atlas.mapkey
        rooms[room_name] = _load_room(room_atlas, default_mapkey, configs,
                                     defaults, player, image_path)

    # Load world
    starting_room = atlas.starting_room
    portals = [] # Waiting for portal implementation
    world = World(rooms, portals, starting_room)

    return world


def _load_configs():
    """Import modules 'terrain', 'item', 'feature', and 'character',
    and return two dicts, one mapping each module to its name and one
    mapping each module's `entities` attribute to its name.
    """
    configs = {}
    defaults = {}
    for archetype in ARCHETYPES:
        configs[archetype] =  __import__(archetype)
        defaults[archetype] = configs[archetype].entities

    return configs, defaults


def _load_atlas():
    """Import and return module 'atlas'."""
    return __import__('atlas')


def load_setting(res_path=RES_PATH):
    """
    Load and return a World instance and the player character instance.
    """
    # Ensure data and resource paths are valid
    _validate_res_path(res_path)

    # Load resources
    image_path = os.path.join(res_path, 'image')
    world_path = os.path.join(res_path, 'world')
    with InsertPath(world_path):
        configs, defaults = _load_configs()
        atlas = _load_atlas()

    # Load player
    player = _load_player(configs['character'].player, image_path)

    # Load world
    world = _load_world(configs, defaults, atlas, player, image_path)

    return world, player
