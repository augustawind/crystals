"""creation and mutation of the game world"""

class Room(list):

    def __init__(self, grid, batch):
        super(Room, self).__init__(grid)
        self.batch = batch
