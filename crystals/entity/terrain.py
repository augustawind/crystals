"""terrain.py - entities that make up the static part of the world"""

from .entity import Entity

class Terrain(Entity):

    def __init__(self, ref, name, image, walkable=True, x_range=0, y_range=0,
            group=None):
        super(Terrain, self).__init__(ref, name, walkable, image, group,
            x_range=x_range, y_range=y_range)

    def __str__(self):
       return 'Terrain'
