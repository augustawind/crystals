rooms = ['TestRoom1']
starting_room = 'TestRoom1'

mapkey = {
    '|': 'wall-vert',
    '-': 'wall-horiz',
    '+': 'floor-smooth',
    ',': 'floor-rough'}


class TestRoom1:

    portalkey = {}

    portals = ()

    mapkey = {}
    
    maps = (
    """
        |-|
        |+|
        |++
    """,
    """
        .,.
        .@. 
        ...
    """)
