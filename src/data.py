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

def load_room(room_dir, hero=None):
    """Returns a world.Room instance, given the name of the directory containing
    information for the Room."""
    # load terrain map file
    map_file = pyglet.resource.file(os.path.join('rooms', room_dir, 'map'), 'r')

    # create ConfigParsers to parse map-key.ini and image-key.ini files
    room_root_dir = os.path.join('data', 'world', 'rooms', room_dir)
    map_key_parser = ConfigParser()
    map_key_parser.read(os.path.join(room_root_dir, 'map-key.ini'))
    image_key_parser = ConfigParser()
    image_key_parser.read(os.path.join(room_root_dir, 'image-key.ini'))

    name = room_dir
    # obtain width and height of room from map-key.ini
    width = map_key_parser.getint('params', 'width')
    height = map_key_parser.getint('params', 'height')

    # construct 3-dimensional list of Terrain instances in Room
    room_map = []
    for row in map_file:
        room_map.append([])
        for symbol in row.strip():
            room_map[-1].append([])
            obj_name = map_key_parser.get('env', symbol)
            image_name = image_key_parser.get('env', obj_name)
            image = images['env.' + image_name]
            obj = getattr(terrain, obj_name)(image)
            room_map[-1][-1].append(obj)

    # add Characters to Room
    char_parser = ConfigParser()
    char_parser.read(os.path.join(room_root_dir, 'char.ini'))
    for section in char_parser.sections():
        image_name = image_key_parser.get('char', section)
        image = images['char.' + image_name]
        if section == 'Hero' and hero:
            char = hero(image)
            hero = char
        else:
            char = getattr(character, section)(image)
        x = char_parser.getint(section, 'x')
        y = char_parser.getint(section, 'y')
        room_map[y][x].append(char)

    # return Room instance, and Hero instance if applicable
    room = world.Room(name, width, height, room_map)
    if hero:
        return room, hero
    else:
        return room

def load_world():
    """Returns a world.World instance from data in the 'data/world' directory.
    """
    # create ConfigParser to parse world.ini file
    parser = ConfigParser()
    parser.read(os.path.join('data', 'world', 'world.ini'))
    # get name of initial room from world.ini
    initial_room_name = parser.get('params', 'initial_room')

    # construct list of Room instances
    rooms = []
    for room_dir in os.listdir(os.path.join('data', 'world', 'rooms')):
        if room_dir == initial_room_name:
            room, hero = load_room(room_dir, character.Hero)
            initial_room = room
        rooms.append(room)

    # return World instance
    return world.World(rooms, initial_room, hero)
