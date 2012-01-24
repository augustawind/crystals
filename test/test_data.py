import os
import sys
import random

import pyglet
from nose.tools import *

import crystals
from crystals import data
from crystals import entity
from test.helpers import *

@raises(data.ResourceError)
def test_ResourceError():
    raise data.ResourceError()


def test_ImageDict():
    for archetype in ('terrain', 'item', 'character', 'interface'):
        images = data.ImageDict(archetype, IMAGE_PATH)

        filenames = os.listdir(os.path.join(IMAGE_PATH, archetype))
        assert len(images) == len(filenames) 
        # Test that each file in img_dir is represented by an entry
        # in `ImageLoader`
        for key, image in images.iteritems():
            assert isinstance(image, pyglet.image.AbstractImage)
            match = False
            for filename in filenames:
                if key == filename.rsplit('.', 1)[0]:
                    match = True
            assert match

def test_InsertPath():
    path = 'foobar'
    with data.InsertPath('foobar'):
        assert 'foobar' in sys.path
    assert 'foobar' not in sys.path


class TestValidateResPath(object):

    def test_valid_path(self):
        data._validate_res_path(RES_PATH)

    @raises(data.ResourceError)
    def test_invalid_path_1(self):
        data._validate_res_path('notapath')

    @raises(data.ResourceError)
    def test_invalid_path_2(self):
        data._validate_res_path(
            os.path.join('test', 'res-invalid-noimage'))

    @raises(data.ResourceError)
    def test_invalid_path_3(self):
        data._validate_res_path(
            os.path.join('test', 'res-invalid-noworld'))

    @raises(data.ResourceError)
    def test_invalid_path_4(self):
        data._validate_res_path(
            os.path.join('test', 'res-invalid-image'))

    @raises(data.ResourceError)
    def test_invalid_path_5(self):
        data._validate_res_path(
            os.path.join('test', 'res_invalid-world'))


def get_world_configs():
    with data.InsertPath(os.path.join(RES_PATH, 'world')):
        configs, defaults = data._load_configs()
        atlas = data._load_atlas()
    return configs, defaults, atlas


def test__load_entity():
    assert isinstance(
        data._load_entity(
            dict(archetype='', name='', walkable=True,
                 image=data.ImageDict('item', IMAGE_PATH)['meat'])),
            entity.Entity)


class ConfigContext(object):

    def __enter__(self):
        class Cfg(object):

            def __init__(self):
                self.configs, self.defaults, self.atlas = get_world_configs()
                self.configs_, self.defaults_, self.atlas_ = get_world_configs()

        self.cfg = Cfg()
        return self.cfg

    def __exit__(self, *exc_args):
        for attr in ('configs', 'defaults', 'atlas'):
            assert (getattr(self.cfg, attr) ==
                    getattr(self.cfg, attr + '_'))


def load_archetype_args(archetype):
    with ConfigContext() as cfg:
        imagedict = data.ImageDict(archetype, IMAGE_PATH)
        return getattr(data, '_load_' + archetype + '_args')(
            'TestRoom1', cfg.configs.get(archetype, {}),
            cfg.defaults.get(archetype, {}), imagedict)


def test__load_global_entity_args():
    # Character needs to be tested, as well as feature and item
    archetype = 'terrain'

    args = load_archetype_args(archetype)
    assert all(type(key) == str for key in args.iterkeys())
    assert all(type(value) == dict for value in args.itervalues())

    keys = ('wall-horiz', 'wall-vert', 'floor-rough', 'floor-smooth')
    names = (
        'a wall', 'towering wall', 'cobbled floor', 'a smooth floor')
    walkables = (False, False, True, True)
              
    for key, name, walkable in zip(keys, names, walkables):
        entity_ = entity.Entity(**args[key])
        assert isinstance(entity_, entity.Entity)
        assert isinstance(entity_, pyglet.sprite.Sprite)
        assert entity_.name == name
        assert entity_.walkable == walkable

def test__load_terrain_args():
    load_archetype_args('terrain')

def test__load_feature_args():
    load_archetype_args('feature')

def test__load_item_args():
    load_archetype_args('item')

def test__load_character_args():
    load_archetype_args('character')
    # ...

def test__load_entity_args():
    with ConfigContext() as cfg:
        args = data._load_entity_args('TestRoom1', cfg.configs, cfg.defaults,
                                      IMAGE_PATH)
    assert all(type(key) == str for key in args.iterkeys())
    assert all(type(value) == dict for value in args.itervalues())

def test__load_portals():
    room1 = crystals.world.Room('TestRoom1', None, [['']])
    room2 = crystals.world.Room('TestRoom2', None, [['']])
    rooms = {'TestRoom1': room1, 'TestRoom2': room2}
    with ConfigContext() as cfg:
        for name, room in rooms.iteritems():
            atlas = getattr(cfg.atlas, name)
            portals = data._load_portals(room, atlas.portals, atlas.portalkey,
                                         rooms)
            assert all(isinstance(p, crystals.world.Portal) for p in portals)
            assert portals[0].from_room.name == name

def test__load_room():
    with ConfigContext() as cfg:
        room_atlas = cfg.atlas.TestRoom1
        default_mapkey = cfg.atlas.mapkey
        player = None
        room1 = data._load_room(room_atlas, default_mapkey, cfg.configs,
                                cfg.defaults, player, IMAGE_PATH)
    assert isinstance(room1, crystals.world.Room)

def test__load_player():
    with ConfigContext() as cfg:
        config = cfg.configs['character'].player
        player = data._load_player(config, IMAGE_PATH)
    assert isinstance(player, entity.Entity)

def test__load_world():
    with ConfigContext() as cfg:
        player = entity.Entity('character', 'player', False,
                                data.ImageDict('character', IMAGE_PATH)['cow'],
                                None)
        world = data._load_world(cfg.configs, cfg.defaults, cfg.atlas,
                                 player, IMAGE_PATH)
        assert isinstance(world, crystals.world.World)

        # rough integrity test for a room in the world -----------------
        room1 = world['TestRoom1']
        archetype = 'terrain'
        img = data.ImageDict(archetype, IMAGE_PATH)
        vwall = entity.Entity(archetype, 'towering wall', False,
                              img['wall-vert-blue'], room1.batch)
        hwall = entity.Entity(archetype, 'a wall', False,
                              img['wall-horiz-blue'], room1.batch)
        floora = entity.Entity(archetype, 'cobbled floor', True,
                               img['floor-a-red'], room1.batch)
        floorb = entity.Entity(archetype, 'a smooth floor', True,
                               img['floor-b-red'], room1.batch)

        room2 = [
            [[vwall, hwall, vwall],
             [vwall, floorb, vwall],
             [vwall, floorb, floorb]
            ],
            [[floora, floora, floora],
             [floora, player, floora],
             [floora, None, None]]]

        for layer1, layer2 in zip(room1, room2):
            for row1, row2 in zip(layer1, reversed(layer2)):
                for e1, e2 in zip(row1, row2):
                    if e1 != None and e2 != None:
                        assert e1.name == e2.name
                        assert e1.walkable == e2.walkable
                        assert e1.batch == e2.batch
                        assert e1.batch == e2.batch

def test__load_configs():
    with ConfigContext() as cfg:
        configs, defaults = data._load_configs()
        assert type(cfg.configs) == dict
        assert all(a in cfg.configs for a in data.ARCHETYPES)
        assert all(a in cfg.defaults for a in data.ARCHETYPES)
        assert all(type(c.entities) == dict for c in cfg.configs.itervalues())
        assert all(c.entities == d for c, d in
                   zip(cfg.configs.itervalues(), cfg.defaults.itervalues()))

def test__load_atlas():
    with ConfigContext() as cfg:
        atlas = data._load_atlas()

def test_load_setting():
    with ConfigContext() as cfg:
        world, player = data.load_setting()
        assert isinstance(world, crystals.world.World)
        assert isinstance(player, entity.Entity)
