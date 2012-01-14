class TestRoom1:

    symbols = {
        '|': 'wall-vert',
        '-': 'wall-horiz',
        '+': 'floor-smooth',
        ',': 'floor-rough'}
    
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
