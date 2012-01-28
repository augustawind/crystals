"""the component parts of a world"""
import pyglet

class Entity(pyglet.sprite.Sprite):
    """A tangible thing in the game world."""

    def __init__(self, archetype, name, walkable, image, batch=None,
                 actions=[]):
        super(Entity, self).__init__(image, batch=batch)
        self.archetype = archetype
        self.name = name
        self.walkable = walkable
        self.batch = batch
        self.actions = actions
