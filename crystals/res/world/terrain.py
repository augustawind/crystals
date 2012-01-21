entities = {
    'bookcase': {
        'params': {
            'name': 'a bookcase',
            'walkable': False,
            'image': 'bookcase'
        },
        'front': {},
        'left': {'variant': 'left'},
        'right': {'variant': 'right'}
    },
    'cave': {
        'params': {
            'name': 'a cave',
            'walkable': True,
            'image': 'cave',
        },
        'dirt': {'variant': 'brown'},
        'stone': {'variant': 'grey'},
        'door': {
            'name': 'a closed door',
            'walkable': False,
            'variant': 'door'
        }
    },
    'door': {
        'open': {
            'name': 'an open door',
            'walkable': True,
            'image': 'door-open'},
        'closed': {
            'name': 'a closed door',
            'walkable': False,
            'image': 'door-closed'},
    },
    'floor': {
        'params': {
            'name': 'a floor',
            'walkable': True
        },
        'rough': {
            'name': 'a rough floor',
            'image': 'floor-a'},
        'smooth': {
            'name': 'a smooth floor',
            'image': 'floor-b'}
    },
    'house': {
        'params': {
            'name': 'a house',
            'walkable': True,
            'image': 'house'
        },
        'a': {'variant': 'a'},
        'b': {'variant': 'b'},
        'c': {'variant': 'c'},
        'd': {'variant': 'd'}
    },
    'stairs': {
        'params': {
            'name': 'a staircase',
            'walkable': True,
            'image': 'stairs'
        },
        'up': {
            'name': 'an ascending staircase',
            'image': 'stairs-up'},
        'down': {
            'name': 'a descending staircase',
            'image': 'stairs-down'}
    },
    'tree': {
        'params': {
            'name': 'a tree',
            'walkable': False
        },
        'green': {'image': 'tree-green'},
        'jungle': {'image': 'tree-jungle'},
        'yellow': {
            'name': 'a yellow tree',
            'image': 'tree-yellow'},
        'leafless': {
            'name': 'a leafless tree',
            'image': 'tree-leafless'},
        'dead': {
            'name': 'a dead tree',
            'image': 'tree-dead'}
    },
    'wall': {
        'params': {
            'name': 'a wall',
            'walkable': False
        },
        'horiz': {
            'image': 'wall-horiz'},
        'vert': {
            'image': 'wall-vert'}
    }
}


class BlueRoom:

    entities = {
        'floor': {
            'params': {
                'variant': 'brown'
            },
            'rough': {},
            'smooth': {},
            'blue': {
                'image': 'floor-b',
                'variant': 'blue'}
        },
        'wall': {
            'params': {
                'variant': 'blue'
            },
            'horiz': {},
            'vert': {},
        },
        'stairs': {
            'up': {'variant': 'blue'}
        },
        'tree': {
            'yellow': {},
            'green': {},
            'leafless': {},
            'dead': {},
            'jungle': {}
        }
    }

class RedRoom:

    entities = {
        'bookcase': {
            'front': {},
            'left': {},
            'right': {}
        },
        'floor': {
            'params': {
                'variant': 'grey'
            },
            'rough': {},
            'smooth': {},
            'red': {'image': 'floor-b-red'}
        },
        'house': {
            'a': {},
            'b': {},
            'c': {},
            'd': {}
        },
        'stairs': {
            'down': {'variant': 'red'}
        },
        'wall': {
            'params': {
                'variant': 'red'
            },
            'horiz': {},
            'vert': {},
        },
    }
