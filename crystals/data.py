"""classes for loading world, image, and sound data"""

import os
from ConfigParser import ConfigParser

import pyglet.resource
import pyglet.font
from pyglet.graphics import OrderedGroup
from pyglet.gl import *

import world
import interaction
from entity import *

glEnable(GL_TEXTURE_2D)

DATA_PATH = os.path.join('crystals', 'data')

# add local fonts to pyglet.font
pyglet.font.add_file(
    os.path.join(DATA_PATH, 'font', 'runescape_uf.ttf'))
pyglet.font.add_file(
    os.path.join(DATA_PATH, 'font', 'terminus.ttf'))

class ImageLoader(dict):
    """A dictionary of game images."""

    def __init__(self):
        """Load images and index them by filename for dict-style access."""
        image_path = os.path.join(DATA_PATH, 'image')
        for directory in os.listdir(image_path):
            self[directory] = {}
            image_subpath = os.path.join(image_path, directory)
            for filename in os.listdir(image_subpath):
                name = filename.rsplit('.', 1)[0]
                image = pyglet.resource.image(
                    os.path.join(image_subpath, filename))
                self[directory][name] = image

class WorldLoader:

    def __init__(self):
        self.images = ImageLoader()
        self.rooms = {}
        self.ignore_symbol = '.'
        self.path = os.path.join(DATA_PATH, 'world')
        self.room_path = os.path.join(self.path, 'rooms')
        self.sections = ['terrain', 'feature', 'item', 'character']

        # load configuration defaults--
        # When a room config file is called upon and data is not present,
        # the data will be obtained from these parsers instead. Only
        # 'world.ini' is required to exist.
        self.parsers = self._get_empty_parser_dict()
        self.parsers['map'].read(os.path.join(self.path, 'map.ini'))
        self.parsers['terrain'].read(os.path.join(self.path, 'terrain.ini'))
        self.parsers['feature'].read(os.path.join(self.path, 'feature.ini'))
        self.parsers['item'].read(os.path.join(self.path, 'item.ini'))
        self.parsers['character'].read(
            os.path.join(self.path, 'character.ini'))

        self._entity_args_loaders = {
            'terrain': self._load_terrain,
            'feature': self._load_feature,
            'item': self._load_item,
            'character': self._load_character}

    # internal interface 
    # -------------------------------------------------------------------------

    def _get_empty_parser_dict(self):
        return dict((parser_name, ConfigParser()) for parser_name in
            self.sections + ['map'])

    def _choose_parser(self, parser, default_parser, section, option):
        if parser.has_option(section, option):
            return parser
        else:
            return default_parser

    def _load_terrain(self, terrain_parser, ref):
        # get walkable
        parser = self._choose_parser(
            terrain_parser, self.parsers['terrain'], ref, 'walkable')
        walkable = parser.getboolean(ref, 'walkable')

        return {'walkable': walkable}

    def _load_item(self, item_parser, ref):
        return {}

    def _load_feature(self, feature_parser, ref):
        return {}

    def _load_character(self, character_parser, ref):
        return {}

    def _load_hero(self, image):
        return character.Hero(image)

    def _load_entity(self, entity_parser, section, ref, group):
        kwargs = {'ref': ref, 'group': group}

        # get name (optional; if none provided, `ref` will be used)
        parser = self._choose_parser(entity_parser,
            self.parsers[section], ref, 'name')
        if parser.has_option(ref, 'name'):
            kwargs['name'] = parser.get(ref, 'name')
        else:
            kwargs['name'] = ref

        # get image
        parser = self._choose_parser(entity_parser,
            self.parsers[section], ref, 'image')
        image_name = parser.get(ref, 'image')
        kwargs['image'] = self.images[section][image_name]

        # scale images
        texture = kwargs['image'].get_texture()
        glBindTexture(GL_TEXTURE_2D, texture.id)
        texture.width = world.TILE_SIZE
        texture.height = world.TILE_SIZE

        if ref == 'hero':
            return self._load_hero(kwargs['image'])

        # get movement ranges (optional)
        parser = self._choose_parser(entity_parser,
            self.parsers[section], ref, 'x-range')
        if parser.has_option(ref, 'x-range'):
            kwargs['x_range'] = parser.getint(ref, 'x-range')
        parser = self._choose_parser(entity_parser,
            self.parsers[section], ref, 'y-range')
        if parser.has_option(ref, 'y-range'):
            kwargs['y_range'] = parser.getint(ref, 'y-range')

        # get section-specific arguments
        kwargs.update(self._entity_args_loaders[section](entity_parser, ref))

        # instantiate entity
        entity = eval(section + '.' + section.title())(**kwargs)

        # add interactions to entity if applicable
        if section in ('character', 'feature'):
            parser = entity_parser
            if (not parser.has_section(entity.ref) or
                not any([option.startswith('interact-')
                    for option in parser.options(entity.ref)])):
                parser = self.parsers[section]
            entity.set_interactions(self._load_interactions(
                dict(parser.items(entity.ref)), entity))

        return entity

    def _load_interactions(self, item_dict, entity):
        interactions = []
        for i in range(len([j for j in item_dict.keys()
                if j.startswith('interact-')])):
            args  = [s.strip() for s in
                item_dict['interact-' + str(i)].strip().split(':')]
            _type = args[0]
            count = int(args[1])
            order = int(args[2])
            sequence = int(args[3])

            if _type == 'text':
                text = args[4].replace('\n', ' ')
                interactions.append(
                    interaction.TextInteraction(count, order, sequence, text))
            elif _type == 'talk':
                speaker = entity
                text = args[4].replace('\n', ' ')
                interactions.append(
                    interaction.TalkInteraction(count, order, sequence, text,
                        speaker))
                
        return interactions

    def _load_portals(self, room_dir):
        """Return list of `world.Portal` instances for a room,
        generated from data in 'portal-key.ini'."""
        portal_parser = ConfigParser()
        portal_parser.read(os.path.join(
            self.room_path, room_dir, 'portal-key.ini'))

        portals = []
        for portal_name in portal_parser.sections():
            x = portal_parser.getint(portal_name, 'x')
            y = portal_parser.getint(portal_name, 'y')
            dest = portal_parser.get(portal_name, 'dest')
            portals.append(world.room.Portal(x, y, portal_name, dest))

        return portals

    def _load_room(self, room_dir, starting_room=False):
        """Returns a world.Room instance, given the name of the directory
        containing config files for the Room. terrain.ini, character.ini, and
        item.ini may be absent if sufficient defaults were provided."""

        room_path = os.path.join(self.room_path, room_dir)

        # load resources ------------------------------------------------------
        map_files = dict((s, []) for s in self.sections)
        for filename in sorted(os.listdir(room_path)):
            if filename.startswith('map-'):
                section = filename.split('-')[1]
                map_files[section].append(pyglet.resource.file(
                    os.path.join(room_path, filename), 'r'))
            
        parsers = self._get_empty_parser_dict()
        parsers['map'].read(os.path.join(room_path, 'map.ini'))
        
        ordered_groups = dict((s, []) for s in self.sections)
        for i in range(len(self.sections)):
            s = self.sections[i]
            parsers[s].read(os.path.join(room_path, s + '.ini'))
            # define OrderedGroups --------------------------------------------
            for j in range(len(map_files[s])):
                if i == 0:
                    ordered_groups[s].append(OrderedGroup(j))
                else:
                    ordered_groups[s].append(OrderedGroup(j +
                        sum([len(ordered_groups[self.sections[i-k]])
                            for k in range(1, i + 1)])))

        # get basic parameters ------------------------------------------------
        name = room_dir
        width = parsers['map'].getint('params', 'width')
        height = parsers['map'].getint('params', 'height')

        # construct empty map -------------------------------------------------
        room_map = [[[] for x in range(width)] for y in range(height)]

        # add entities --------------------------------------------------------
        interact_entities = []
        for section, files in map_files.items():
            for i in range(len(files)):
                map_file = files[i]
                for y in range(height):
                    row = map_file.readline().strip()
                    for x in range(width):
                        symbol = row[x]

                        # continue if 'nothing' symbol encountered
                        if symbol == self.ignore_symbol:
                            continue

                        # get entity ref
                        parser = self._choose_parser(parsers['map'],
                            self.parsers['map'], section, symbol)
                        ref = parser.get(section, symbol)
                        
                        # instantiate entity
                        entity = self._load_entity(parsers[section],
                            section, ref, ordered_groups[section][i])
                        if ref == 'hero':
                            hero = entity

                        # add entity to map
                        room_map[y][x].append(entity)
                map_file.close()

        # remove bluriness from scaled images
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # reverse map
        room_map.reverse()

        # add portals to room -------------------------------------------------
        portals = self._load_portals(room_dir)

        # return `Room` instance, plus `Hero` instance if appl.
        room = world.room.Room(name, width, height, room_map, portals)
        if starting_room:
            return room,  hero
        else:
            return room

    # public interface
    # -------------------------------------------------------------------------

    def load_world(self):
        """Return a `world.World` instance from data in the 'data/world'
        directory."""
        # load rooms ----------------------------------------------------------
        starting_room_name = self.parsers['map'].get('params', 'starting_room')

        for room_dir in os.listdir(self.room_path):
            if room_dir == starting_room_name:
                room, hero = self._load_room(room_dir, True)
                starting_room = room
            else:
                room = self._load_room(room_dir)

            self.rooms[room_dir] = room

        # return `world.World` instance ---------------------------------------
        return world.World(self.rooms, starting_room, hero)
