"""data.py"""
import os
from ConfigParser import ConfigParser

import pyglet.resource

import world
import terrain
import character
import interaction

pyglet.resource.path = ['data', 'data/image', 'data/world']
pyglet.resource.reindex()

class ImageLoader(dict):
    """A dictionary of game images."""

    def __init__(self):
        """Load images and index them by filename for dict-style access."""
        root = os.path.join('data', 'image')
        for directory in os.listdir(root):
            for filename in os.listdir(os.path.join(root, directory)):
                name = directory + '.' + filename.rsplit('.', 1)[0]
                self[name] = pyglet.resource.image(
                    os.path.join(directory, filename))

images = ImageLoader()

def load_interactable(item_dict):
    name = item_dict['interact-object']
    count = int(item_dict['interact-count'])

    if name == 'TextInteractable':
        text = item_dict['interact-text']
        return getattr(interaction, name)(count, text)
        

def load_room(room_dir, default_map_key, default_image_key,
        default_terrain_parser, default_character_parser, starting_room=None):
    """Returns a world.Room instance, given the name of the directory containing
    config files for the Room. All files must be present. If relevant data is
    not present in image-key.ini and map-key.ini, `default_image_key` and
    `default_map_key` will be searched, respectively."""

    # load resources ----------------------------------------------------------
    map_file = pyglet.resource.file(os.path.join('rooms', room_dir, 'map'), 'r')

    room_root_dir = os.path.join('data', 'world', 'rooms', room_dir)

    map_key = ConfigParser()
    map_key.read(os.path.join(room_root_dir, 'map-key.ini'))
    image_key = ConfigParser()
    image_key.read(os.path.join(room_root_dir, 'image-key.ini'))
    character_parser = ConfigParser()
    character_parser.read(os.path.join(room_root_dir, 'character.ini'))
    terrain_parser = ConfigParser()
    terrain_parser.read(os.path.join(room_root_dir, 'terrain.ini'))

    # get basic parameters ----------------------------------------------------
    name = room_dir
    width = map_key.getint('params', 'width')
    height = map_key.getint('params', 'height')

    # construct room map ------------------------------------------------------
    ordered_entities = [[], [], []]
    room_map = []
    for row in map_file:
        room_map.append([])
        for symbol in row.strip():
            room_map[-1].append([])

            # get terrain name
            if map_key.has_option('terrain', symbol):
                terrain_name = map_key.get('terrain', symbol)
            else:
                terrain_name = default_map_key.get('terrain', symbol)

            # get terrain walkable status
            if terrain_parser.has_option(terrain_name, 'walkable'):
                walkable = terrain_parser.getboolean(terrain_name, 'walkable')
            else:
                walkable = default_terrain_parser.getboolean(terrain_name,
                    'walkable')

            # get terrain image
            if image_key.has_option('terrain', terrain_name):
                image_name = image_key.get('terrain', terrain_name)
            else:
                image_name = default_image_key.get('terrain', terrain_name)
            image = images['terrain.' + image_name]

            # instantiate terrain object and add to room
            terrain_obj = terrain.Terrain(terrain_name, walkable, image)
            room_map[-1][-1].append(terrain_obj)
            ordered_entities[0].append(terrain_obj)
    map_file.close()

    # add characters to room --------------------------------------------------
    for character_name in character_parser.sections():
        # get character image
        if image_key.has_option('character', character_name):
            image_name = image_key.get('character', character_name)
        else:
            image_name = default_image_key.get('character', character_name)
        image = images['character.' + image_name]

        # determine whether character is Hero or not
        if character_name == 'Hero' and starting_room:
            # instantiate Hero
            character_obj = character.Hero(image)
            hero = character_obj
        else:
            # get `Interactable` object for non-player character
            if character_parser.has_option(character_name, 'interact-object'):
                interactable = load_interactable(
                    dict(character_parser.items(character_name)))
            else:
                interactable = load_interactable(
                    dict(default_character_parser.items(character_name)))
            # instantiate non-player character
            character_obj = character.Character(
                character_name, image, interactable)

        # add character to map and entities list
        x = character_parser.getint(character_name, 'x')
        y = character_parser.getint(character_name, 'y')
        room_map[y][x].append(character_obj)
        ordered_entities[2].append(character_obj)

    # return `Room` instance, list of entities, and `Hero` instance if appl.
    room = world.Room(name, width, height, room_map)
    if starting_room:
        return room, ordered_entities, hero
    else:
        return room, ordered_entities

def load_portals(room_dir, rooms):
    """Return list of `world.Portal` instances for a room,
    generated from data in 'portal-key.ini'."""
    portal_key = ConfigParser()
    portal_key.read(os.path.join(
        'data', 'world', 'rooms', room_dir, 'portal-key.ini'))

    portals = []
    for room_name in portal_key.sections():
        x = portal_key.getint(room_name, 'x')
        y = portal_key.getint(room_name, 'y')
        room = rooms[room_name]
        portals.append(world.Portal(x, y, room))

    return portals

def load_world():
    """Return a `world.World` instance from data in the 'data/world' directory.
    """
    # load resources ----------------------------------------------------------
    root_dir = os.path.join('data', 'world')

    world_key = ConfigParser()
    world_key.read(os.path.join(root_dir, 'world-key.ini'))
    map_key = ConfigParser()
    map_key.read(os.path.join(root_dir, 'map-key.ini'))
    image_key = ConfigParser()
    image_key.read(os.path.join(root_dir, 'image-key.ini'))
    terrain_parser = ConfigParser()
    terrain_parser.read(os.path.join(root_dir, 'terrain.ini'))
    character_parser = ConfigParser()
    character_parser.read(os.path.join(root_dir, 'character.ini'))

    # get name of starting room from world.ini
    starting_room_name = world_key.get('params', 'starting_room')

    # load rooms --------------------------------------------------------------
    ordered_entities = [[], [], []]
    rooms = {}
    for room_dir in os.listdir(os.path.join('data', 'world', 'rooms')):
        if room_dir == starting_room_name:
            room, entities, hero = load_room(room_dir, map_key, image_key,
                terrain_parser, character_parser, True)
            starting_room = room
        else:
            room, entities = load_room(room_dir, map_key, image_key,
                terrain_parser, character_parser)
        rooms[room_dir] = room

        for i in range(len(entities)):
            ordered_entities[i].extend(entities[i])

    # add portals to rooms ----------------------------------------------------
    for room_name, room in rooms.items():
        portals = load_portals(room_name, rooms)
        room.add_portals(*portals)

    # return `world.World` instance -------------------------------------------
    return world.World(rooms, starting_room, hero, ordered_entities)
