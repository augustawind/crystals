"""tools for loading game resources"""
import os

import pyglet

from crystals import entity

RES_PATH = os.path.join('crystals', 'res') # default path to game resources
ENTITY_TYPES = ('terrain', 'item', 'character') # entity sub-categories

class ImageDict(dict):
    """Loads game images."""

    def __init__(self, img_dir, res_path=RES_PATH):
        """Load all images in `img_dir`, where `img_dir` is a
        directory in data/images.

        Images can then be accessed dict-style, where each key is an
        image's filename without the extension, e.g. 'human-peasant'
        for 'human-peasant.png'.
        """
        path = os.path.join(res_path, 'image', img_dir)
        for filename in os.listdir(path):
            key = filename.rsplit('.', 1)[0]
            image = pyglet.image.load(os.path.join(path, filename))
            self[key] = image


class WorldLoader(object):
    """Loads the game world."""

    def __init__(self, res_path=RES_PATH):
        self.res_path = res_path
        self.world_path = os.path.join(self.res_path, 'world')
        self.room_path = os.path.join(self.world_path, 'rooms')
        self.rooms = {}
        self.images = dict.fromkeys(ENTITY_TYPES)

    def load_images(self, entity_type):
        """Load all images for the given entity type."""
        self.images[entity_type] = ImageDict(entity_type, self.res_path)

    def load_entity(self, name, walkable, image):
        """Return an Entity object with the given parameters."""
        return entity.Entity(name, walkable, image)

    def load_entities(self, entity_type):
        images = ImageDict(entity_type)
        config = __import__('crystals.world.config.' + entity_type,
                            fromlist=['archetypes', 'entities'])

        entities = {}
        for archetype_name, archetype in config.entities.iteritems():
            default_params = config.archetypes[archetype_name]
            for entity_name, params in archetype.iteritems():
                # If name is not given in any params, generate one
                if 'name' not in params and 'name' not in default_params:
                    params['name'] = archetype_name + '-' + entity_name
                # Replace missing entries from params with entries from
                # default_params
                for key in ('name', 'walkable', 'image', 'color', 'symbol'):
                    if key not in params:
                        params[key] = default_params[key]
                # Combine image and color params to get the image name
                params['image'] += '-' + params.pop('color')
                # Load the image
                params['image'] = images[params['image']]
                
                symbol = params.pop('symbol')
                entities[symbol] = entity.Entity(**params)

        return entities

    def load_world(self):pass
