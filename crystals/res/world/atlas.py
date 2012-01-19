symbols = {
    '|': 'wall-vert',
    '-': 'wall-horiz',
    '+': 'floor-smooth',
    ',': 'floor-rough',

    '?': 'tree-green',
    'Y': 'tree-yellow',
    'l': 'tree-leafless',
    '7': 'tree-dead',
    '!': 'tree-jungle'}


class BlueRoom:

    symbols = {}
    
    maps = (
    """
+++++++++++
+,++,+,++,+
++,++,++,++
+++,+++,+++
+,++,+,++,+
++,++,++,++
+,++,+,++,+
+++,+++,+++
++,++,++,++
+,++,+,++,+
+++++++++++
    """,
    """
|---------|
|.........|
|.........|
|.........|
|.........|
|.........|
|.........|
|.........|
|.........|
|.........|
|---------|
    """,
    """
...........
...........
.....Y.....
...........
.....l.....
..Y.l7l.Y..
.....l.....
...........
.....Y.....
...........
...........
    """,
    """
...........
...........
...........
...........
...........
...........
...........
...........
...........
.......@...
...........
    """)


rooms = ['BlueRoom']
starting_room = 'BlueRoom'
