"""terrain.py"""

from world import Entity

class Terrain(Entity):

    def __init__(self, name, walkable, image):
        super(Terrain, self).__init__(name, walkable, image)

    def __str__(self):
        return 'Terrain'

class Wall(Terrain):
    
    def __init__(self, image):
        super(Wall, self).__init__('Wall', False, image)

class Floor(Terrain):

    def __init__(self, image):
        super(Floor, self).__init__('Floor', True, image)

class Tree(Terrain):

    def __init__(self, image):
        super(Tree, self).__init__('Tree', False, image)

class Door(Terrain):

    def __init__(self, image):
        super(Door, self).__init__('Door', True, image)
