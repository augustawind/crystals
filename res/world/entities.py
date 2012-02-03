# define archetype classes ---------------------------------------------
class terrain(object):
    name = 'feature of the environment'
    walkable = True

class character(object):
    name = 'intelligent life form'
    walkable = False

# define player --------------------------------------------------------
class player(character):
    name = 'supercow'
    image = 'cow.png'

# define terrain template classes --------------------------------------
class xterrain(terrain):
    name = 'blockade of some sort'
    walkable = False

class floor(terrain):
    name = 'surface'
    image = 'floor-'
class floor_rough(floor):
    name = 'rough surface'
    image = floor.image + 'a-'
class floor_smooth(floor):
    name = 'smooth surface'
    image = floor.image + 'b-'

class wall(xterrain):
    name = 'wall'
    image = 'wall-'
class vwall(wall):
    image = wall.image + 'vert-'
class hwall(wall):
    image = wall.image + 'horiz-'

# define rooms
# ----------------------------------------------------------------------

class RedRoom(object):

    ALL = ['floor_rough', 'floor_smooth']

    class floor_rough(floor_rough):
        image = floor_rough.image + 'red.png'
    class floor_smooth(floor_smooth):
        image = floor_smooth.image + 'red.png'

    class vwall(vwall):
        image = vwall.image + 'red.png'
    class hwall(hwall):
        image = hwall.image + 'red.png'
