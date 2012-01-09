import pyglet

class Entity(pyglet.sprite.Sprite):
    """A tangible thing in the game world."""

    def __init__(self, name, walkable, image, batch=None):
        super(Entity, self).__init__(image, batch=batch)
        self.name = name
        self.walkable = walkable
        self.batch = batch
