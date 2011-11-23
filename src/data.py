"""data.py"""
import os
from ConfigParser import ConfigParser

import pyglet.resource

import world
import terrain
import character

pyglet.resource.path = ['data', 'data/img', 'data/world']
pyglet.resource.reindex()

class ImageLoader(dict):
    """A dictionary of game images."""

    def __init__(self):
        """Load images and index them by filename for dict-style access."""
        root = os.path.join('data', 'img')
        for directory in os.listdir(root):
            for filename in os.listdir(os.path.join(root, directory)):
                name = directory + '.' + filename.rsplit('.', 1)[0]
                self[name] = pyglet.resource.image(
                    os.path.join(directory, filename))

images = ImageLoader()

def load_room(room_dir, default_map_key, default_image_key, hero=None):
    """Returns a world.Room instance, given the name of the directory containing
    config files for the Room. All files must be present. If relevant data is
    not present in image-key.ini and map-key.ini, `default_image_key` and
    `default_map_key` will be searched, respectively."""
    # load terrain map file
    map_file = pyglet.resource.file(os.path.join('rooms', room_dir, 'map'), 'r')

    room_root_dir = os.path.join('data', 'world', 'rooms', room_dir)

    # create ConfigParsers to parse map-key.ini and image-key.ini files
    map_key = ConfigParser()
    map_key.read(os.path.join(room_root_dir, 'map-key.ini'))
    image_key = ConfigParser()
    image_key.read(os.path.join(room_root_dir, 'image-key.ini'))

    name = room_dir
    width = map_key.getint('params', 'width')
    height = map_key.getint('params', 'height')

    # ordered_entities list; determines rendering order of entities
    ordered_entities = [[], [], []]

    room_map = []
    # construct 3-dimensional list of Terrain instances in Room
    for row in map_file:
        room_map.append([])
        for symbol in row.strip():
            room_map[-1].append([])

            if map_key.has_option('env', symbol):
                obj_name = map_key.get('env', symbol)
            else:
                obj_name = default_map_key.get('env', symbol)
            if image_key.has_option('env', obj_name):
                image_name = image_key.get('env', obj_name)
            else:
                image_name = default_image_key.get('env', obj_name)

            image = images['env.' + image_name]
            obj = getattr(terrain, obj_name)(image)
            room_map[-1][-1].append(obj)
            ordered_entities[0].append(obj)

    map_file.close()

    # add Characters to Room
    char_parser = ConfigParser()
    char_parser.read(os.path.join(room_root_dir, 'char.ini'))

    for section in char_parser.sections():
        if image_key.has_option('char', section):
            image_name = image_key.get('char', section)
        else:
            image_name = default_image_key.get('char', section)
        image = images['char.' + image_name]

        if section == 'Hero' and hero:
            char = hero(image)
            hero = char
        else:
            char = getattr(character, section)(image)

        x = char_parser.getint(section, 'x')
        y = char_parser.getint(section, 'y')
        room_map[y][x].append(char)
        ordered_entities[2].append(obj)

    # return Room instance, and Hero instance if applicable
    room = world.Room(name, width, height, room_map)
    if hero:
        return room, ordered_entities, hero
    else:
        return room, ordered_entities

def load_portals(room_dir, rooms):
    portals = []
    portal_key = ConfigParser()
    portal_key.read(os.path.join(
        'data', 'world', 'rooms', room_dir, 'portal-key.ini'))
    for room_name in portal_key.sections():
        x = portal_key.getint(room_name, 'x')
        y = portal_key.getint(room_name, 'y')
        room = rooms[room_name]
        portals.append(world.Portal(x, y, room))

    return portals

def load_world():
    """Returns a world.World instance from data in the 'data/world' directory.
    """
    root_dir = os.path.join('data', 'world')
    # create ConfigParser to parse world.ini file
    world_key = ConfigParser()
    world_key.read(os.path.join(root_dir, 'world-key.ini'))
    # get name of initial room from world.ini
    initial_room_name = world_key.get('params', 'initial_room')

    # create ConfigParser to parse map-key.ini
    map_key = ConfigParser()
    map_key.read(os.path.join(root_dir, 'map-key.ini'))
    # create ConfigParser to parse image-key.ini
    image_key = ConfigParser()
    image_key.read(os.path.join(root_dir, 'image-key.ini'))

    # ordered_entities list
    ordered_entities = [[], [], []]

    # construct dict of Room instances indexed by name
    rooms = {}
    for room_dir in os.listdir(os.path.join('data', 'world', 'rooms')):
        if room_dir == initial_room_name:
            room, entities, hero = load_room(
                room_dir, map_key, image_key, character.Hero)
            initial_room = room
        else:
            room, entities = load_room(room_dir, map_key, image_key)
        rooms[room_dir] = room

        for i in range(len(entities)):
            ordered_entities[i].extend(entities[i])

    # add Portals to Rooms
    for room_name, room in rooms.items():
        portals = load_portals(room_name, rooms)
        room.add_portals(*portals)

    # return World instance
    return world.World(rooms, initial_room, hero, ordered_entities)
