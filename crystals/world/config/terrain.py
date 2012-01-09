archetypes = {
    'floor': {'walkable': True,
              'color': 'red'},
    'wall': {'name': 'wall',
             'walkable': False,
             'color': 'blue'}
    }

entities = {
    'floor': {
        'rough': {
            'name': 'cobbled floor',
            'image': 'floor-a',
            'symbol': ','},
        'smooth': {
            'image': 'floor-b',
            'symbol': '+'}},
    'wall': {
        'horiz': {
            'image': 'wall-horiz',
            'symbol': '-'},
        'vert': {
            'name': 'towering wall',
            'image': 'wall-vert',
            'symbol': '|'}}
    }
