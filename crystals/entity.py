import pyglet

class Entity(object):
    """A tangible thing in the game world."""

    def __init__(self, name, walkable, image):
        self.name = name
        self.walkable = walkable
        self.sprite = pyglet.sprite.Sprite(image)
