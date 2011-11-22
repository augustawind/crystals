"""terrain.py"""

from world import Entity

class Terrain(Entity):

    def __init__(self, name, walkable, image):
        super(Terrain, self).__init__(name, walkable, image)

class Wall(Terrain):
    
    def __init__(self, image):
        super(Wall, self).__init__('Wall', False, image)

class Floor(Terrain):

    def __init__(self, image):
        super(Floor, self).__init__('Floor', True, image)

class Tree(Terrain):

    def __init__(self, image):
        super(Tree, self).__init__('Tree', False, image)
