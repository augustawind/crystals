from collections import namedtuple

# Define some template entities

entity = namedtuple('entity', 'name walkable image')

rfloor = entity('rough surface', True, 'floor-a-')
sfloor = entity('smooth surface', True, 'floor-b-')

wall = entity('wall', False, None)
vwall = wall._replace(image='wall-vert-')
hwall = wall._replace(image='wall-horiz-')

# Define entities for each room
# ----------------------------------------------------------------------

class RedRoom:

    ALL = ['rfloor', 'sfloor', 'vwall', 'hwall']

    rfloor = rfloor._replace(image=rfloor.image + 'red.png')
    sfloor = sfloor._replace(image=sfloor.image + 'red.png')

    vwall = vwall._replace(image=vwall.image + 'blue.png')
    hwall = hwall._replace(image=hwall.image + 'blue.png')
