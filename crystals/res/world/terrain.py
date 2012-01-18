entities = {
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
            'walkable': True
        },
        'rough': {
            'name': 'a rough floor',
            'image': 'floor-a'},
        'smooth': {
            'name': 'a smooth floor',
            'image': 'floor-b'}
    },
    'stairs': {
        'params': {
            'walkable': True
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
        'green': {
            'image': 'tree-green'},
        'yellow': {
            'name': 'a yellow tree',
            'image': 'tree-yellow'},
        'leafless': {
            'name': 'a leafless tree',
            'image': 'tree-leafless'},
        'dead': {
            'name': 'a dead tree',
            'image': 'tree-dead'},
        'jungle': {
            'image': 'tree-jungle'}
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
                'variant': 'grey'
            },
            'rough': {},
            'smooth': {}
            },
        'wall': {
            'params': {
                'variant': 'blue'
            },
            'horiz': {},
            'vert': {},
        },
        'tree': {
            'yellow': {},
            'green': {},
            'leafless': {},
            'dead': {},
            'jungle': {}
        }
    }
