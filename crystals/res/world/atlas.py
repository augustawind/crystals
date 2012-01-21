rooms = ['BlueRoom']
starting_room = 'BlueRoom'

mapkey = {
    '+': 'floor-smooth',
    ',': 'floor-rough',

    '<': 'stairs-up',
    '>': 'stairs-down',

    '?': 'tree-green',
    'Y': 'tree-yellow',
    'l': 'tree-leafless',
    '7': 'tree-dead',
    '!': 'tree-jungle',

    '|': 'wall-vert',
    '-': 'wall-horiz'
}


class BlueRoom:

    portalkey = {
        'r': 'RedRoom'
    }

    portals = (
    """
...........
...........
...........
...........
...........
.........r.
...........
...........
...........
...........
...........
    """
    )

    mapkey = {
        '*': 'floor-blue'
    }
    
    maps = (
    """
+++++++++++
+,++,*,++,+
++,++*++,++
+++,+*+,+++
+,++***++,+
+*********+
+,++***++,+
+++,+*+,+++
++,++*++,++
+,++,*,++,+
+++++++++++
    """,
    """
|---------|
|.........|
|....Y....|
|.........|
|....l....|
|.Y.l7l..<|
|....l....|
|.........|
|....Y....|
|......@..|
|||||||||||
    """)


class RedRoom:
    pass
