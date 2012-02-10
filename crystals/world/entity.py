"""the component parts of a world"""
import pyglet

class Entity(pyglet.sprite.Sprite):
    """A tangible thing in the game world."""

    def __init__(self, name, walkable, image, batch=None,
                 facing=(0, -1), actions=[], x=0, y=0):
        super(Entity, self).__init__(image, batch=batch)
        self.name = name
        self.walkable = walkable
        self.batch = batch
        self._facing = facing
        self.actions = actions
        self._x = x
        self._y = y

    @property
    def facing(self):
        return self._facing
    
    @facing.setter
    def facing(self, xy):
        x, y = xy
        self._facing = (x, y)
