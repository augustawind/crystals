rooms = ['TestRoom1', 'TestRoom2']
starting_room = 'TestRoom1'

mapkey = {
    '|': 'wall-vert',
    '-': 'wall-horiz',
    '+': 'floor-smooth',
    ',': 'floor-rough'}


class TestRoom1:

    mapkey = {}
    
    maps = [
    """
|-|
|+|
|++
    """,
    """
.,.
.@. 
...
    """
    ]

    portalkey = {
        '2': 'TestRoom2'}

    portals = """
...
...
..2
    """


class TestRoom2:

    mapkey = {'>': 'stairs-down'}
    
    maps = [
    """
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
    """,
    """
.....
.....
..>..
.....
.....
    """
    ]

    portalkey = {
        '1': 'TestRoom1'}

    portals = """
.....
.....
..1..
.....
.....
    """
