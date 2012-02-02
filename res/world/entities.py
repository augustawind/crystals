from crystals.res.world.util import img

entities = [
    'terrain', 'character', 'xterrain', 'vwall', 'hwall', 'floor_smooth',
    'floor_rough'] 


def img(*parts):
    """Convenience function for providing the image names for entities."""
    ext = '.png'
    for part in parts:
        part.replace(ext, '')

    if not parts:
        return ''
    if len(parts) == 1:
        return parts[0]
    return '-'.join(parts) + ext


# define archetype classes ---------------------------------------------
class terrain(object):
    name = 'feature of the environment'
    archetype = 'terrain'
    walkable = True
    image = img()

class character(object):
    name = 'intelligent life form'
    archetype = 'character'
    walkable = False
    image = img()

# define player --------------------------------------------------------
class player(character):
    name = 'supercow'
    image = img('cow')

# define terrain template classes --------------------------------------
class xterrain(terrain):
    name = 'blockade of some sort'
    walkable = False

class wall(xterrain):
    name = 'wall'
    image = img('wall')
class vwall(wall): image = img(wall.image, 'vert')
class hwall(wall): image = img(wall.image, 'horiz')

class floor(terrain):
    name = 'surface'
    image = img('floor')
class floor_smooth(floor):
    name = 'smooth surface'
    image = img(floor.image, 'smooth')
class floor_rough(floor):
    name = 'rough surface'
    image = img(floor.image, 'rough')


class TestRoom1(object):

    entities = ['floor_rough', 'floor_smooth']

    class floor_rough(floor_rough):
        name = 'cobbled floor'
        image = img(floor_rough.image, 'red')
    class floor_smooth(floor_smooth):
        image = img(floor_smooth.image, 'red')
