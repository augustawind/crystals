from pyglet.sprite import Sprite 

class Entity(Sprite):
    """A tangible thing. Populates Rooms."""

    def __init__(self, ref, name, walkable, image, group, interactions=[],
            x_range=0, y_range=0):
        super(Entity, self).__init__(image, group=group)

        self._ref = ref
        self._name = name
        self._walkable = walkable
        self._interactions = interactions
        self._x_range = x_range
        self._y_range = y_range

        self._tether_x = 0
        self._tether_y = 0

    @property
    def ref(self):
        return self._ref

    @property
    def name(self):
        return self._name

    @property
    def walkable(self):
        return self._walkable

    @property
    def interactable(self):
        return bool(self._interactions)

    def set_interactions(self, interactions):
        print '{}.set_interactions'.format(self.name)
        print '\tinteractions={}'.format([str(i) for i in interactions])
        print 'before, {}._interactions ='.format(self.name), self._interactions
        self._interactions = interactions
        print 'after, {}._interactions ='.format(self.name), self._interactions
        print
    
    def iter_interactions(self):
        return iter(sorted(self._interactions, key=lambda x: x.sequence))

    def set_tether(self, x, y):
        self._tether_x = x
        self._tether_y = y

    def is_in_range(self, x, y):
        """Return True if (x, y) is between the character's tether and
        (x_range, y_range) for each direction."""
        return (
            ((self._x_range == -1) or (self._tether_x - self._x_range <= x <=
                self._tether_x + self._x_range)) and
            ((self._y_range == -1) or (self._tether_y - self._y_range <= y <=
                self._tether_y + self._y_range)))
