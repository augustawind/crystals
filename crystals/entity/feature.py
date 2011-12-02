"""feature.py - interactable terrain entities"""

from .entity import Entity

class Feature(Entity):
    
    def __init__(self, name, walkable, image, interactable,
            x_range=0, y_range=0):
        super(Feature, self).__init__(name , walkable, image, interactable,
            x_range, y_range)

    def __str__(self):
        return 'Feature'
