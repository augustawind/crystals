symbols = {
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

    symbols = {
        '*': 'floor-blue'}

    portals = ()
    
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
|....l<...|
|.Y.l7l.Y.|
|....l....|
|.........|
|....Y....|
|......@..|
|||||||||||
    """)


class RedRoom:

    symbols = {}

    portals = ()

    maps = ()


rooms = ['BlueRoom']
starting_room = 'BlueRoom'
