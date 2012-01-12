"""creation and mutation of the game world"""

TILE_SIZE = 24

class Room(list):

    def __init__(self, name, batch, layers):
        super(Room, self).__init__(layers)
        self.name = name
        self.batch = batch

        for layer in self:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    entity = layer[y][x]
                    if entity is not None:
                        self._update_entity(entity, x, y)

    def _update_entity(self, entity, x, y):
        entity.batch = self.batch
        entity.set_position(x * TILE_SIZE, y * TILE_SIZE)


class World(dict):

    def __init__(self, rooms, current_room):
        super(World, self).__init__(rooms)
        self.focus = current_room
