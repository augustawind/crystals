
def load_room(name, atlas, entities):
    """Return a Room instance, given its name, object `atlas` describing
    its layout and object `entities` describing its entities.
    """
    grid = []
    # Read rows in reverse so that maps displayed in symbol form
    # in the atlas mirror the actual appearance of the room
    for rows in reversed(zip(*atlas.map)):
        grid.append([])
        for cell in zip(*rows):
            grid[-1].append([])
            for z, char in enumerate(cell):
                if char == IGNORE_CHAR:
                    entity = None
                else:
                    entity = getattr(entities, atlas.key[char])()
                    prepare_sprite(entity)
                grid[-1][-1].append(entity)

    return Room(name, grid)


def load_portals(atlas):
    """Return a list mapping room names to [y][x] indicies indicating
    portal locations and their destination rooms, given object `atlas`
    describing their positions and destination rooms.
    """
    portals = {}
    for y in reversed(xrange(len(atlas.portalmap))):
        for x, char in enumerate(atlas.portalmap[y]):
            if char == IGNORE_CHAR:
                continue
            dest = atlas.portalkey[char]
            portals[dest] = (x, y)

    return portals
