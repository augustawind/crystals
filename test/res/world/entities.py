# define archetype classes ---------------------------------------------
class terrain(object):
    name = 'feature of the environment'
    archetype = 'terrain'
    walkable = True
    image = ''

class character(object):
    name = 'intelligent life form'
    archetype = 'character'
    walkable = False
    image = ''

# define terrain template classes --------------------------------------
class xterrain(terrain):
    name = 'blockade of some sort'
    walkable = False

class wall(xterrain):
    name = 'wall'
    image += 'wall'

class floor(terrain):
    name = 'floor'
    image += 'floor'


# begin old code -------------------------------------------------------
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


class TestRoom1:

    entities = {
        'floor': {
            'params': {
                'variant': 'red'
            },
            'rough': {'name': 'cobbled floor'},
            'smooth': {}
            },
        'wall': {
            'params': {
                'variant': 'blue'
            },
            'horiz': {},
            'vert': {'name': 'towering wall'},
        }
    }


class TestRoom2:

    entities = {
        'floor': {
            'rough': {'variant': 'red'}
            },
        'stairs': {
            'down': {'variant': 'red'}
        }
    }
