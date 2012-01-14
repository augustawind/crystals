symbols = {
    '|': 'wall-vert',
    '-': 'wall-horiz',
    '+': 'floor-smooth',
    ',': 'floor-rough'}


class TestRoom1:

    symbols = {}
    
    maps = (
    """
        |-|
        |+|
        |++
    """,
    """
        .,.
        ... 
        ...
    """)


rooms = ['TestRoom1']
starting_room = 'TestRoom1'
