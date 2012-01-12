"""creation and mutation of the game world"""

TILE_SIZE = 24

class Room(list):

    def __init__(self, grid, batch):
        super(Room, self).__init__(grid)
        self.batch = batch
