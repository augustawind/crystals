"""creation and mutation of the game world"""

TILE_SIZE = 24

class Room(list):

    def __init__(self, batch, layers):
        super(Room, self).__init__(layers)
        self.batch = batch

        for layer in self:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    entity_ = layer[y][x]
                    if entity_ is not None:
                        self._update_entity(entity_, x, y)

    def _update_entity(self, entity, x, y):
        entity.batch = self.batch
        entity.set_position(x * TILE_SIZE, y * TILE_SIZE)

class World(list):

    def __init__(self, batch, rooms):
        super(World, self).__init__(rooms)
        self.batch = batch

