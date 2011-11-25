"""terrain.py"""

from world import Entity

class Terrain(Entity):

    def __init__(self, name, walkable, image, interactable=None):
        super(Terrain, self).__init__(name, walkable, image, interactable)

    def __str__(self):
        return 'Terrain'

class Wall(Terrain):
    
    def __init__(self, image, interactable=None):
        super(Wall, self).__init__('Wall', False, image, interactable=None)

class Floor(Terrain):

    def __init__(self, image, interactable=None):
        super(Floor, self).__init__('Floor', True, image, interactable=None)

class Tree(Terrain):

    def __init__(self, image, interactable=None):
        super(Tree, self).__init__('Tree', False, image, interactable=None)

class Door(Terrain):

    def __init__(self, image, interactable=None):
        super(Door, self).__init__('Door', True, image, interactable=None)
