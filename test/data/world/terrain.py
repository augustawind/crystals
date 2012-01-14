class TestRoom1:

    defaults = {
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
                'image': 'floor-a'},
            'smooth': {
                'image': 'floor-b'}},
        'wall': {
            'horiz': {
                'image': 'wall-horiz'},
             'vert': {
                'name': 'towering wall',
                'image': 'wall-vert'}}
        }
