"""terrain.py - entities that make up the static part of the world"""

from world import Entity

class Terrain(Entity):

    def __init__(self, name, walkable, image, interactable=None):
        super(Terrain, self).__init__(name, walkable, image, interactable)

    def __str__(self):
        return 'Terrain'
