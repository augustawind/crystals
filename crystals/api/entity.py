from crystals.world import Entity as _Entity

EntityArgs = namedtuple(
    'EntityArgs', ['name', 'walkable', 'image', 'action', 'facing', 'id'])
EntityArgs.__doc___ = (
    """A named tuple whose fields are identical to `Entity` arguments."""

# Define default args such that only 'image' need be provided
defaultargs = EntityArgs('', False, '', None, (0, -1), None)

def entity(parent=defaultargs):
    """A decorator factory for entity definitions.
    
    Given a parent `EntityArgs` instance, return a decorator whose 
    target is replaced by an `EntityArgs` instance with the given
    arguments, after undergoing the following transformations:
    
        1. Positional arguments are converted to keyword arguments.
        1. If argument ``image`` is a format string, format it with
           the entire argument dict. Coupled with patterned naming
           practices for image resources, this could be used to define
           a markup language for entity aesthetics.
           aesthetics
        2. For each field in `EntityArgs` that does not have a value in
           the given arguments (positionally or keyword) obtain the value
           from `parent`.

    The returned `EntityArgs` instance can be called to return an
    `Entity` instance with the transformed given arguments.
    """
    def decorator(func):
        def wrapped(*args, **kwargs):
            kwargs.update(zip(EntityArgs._fields, args))
            kwargs['image'] = kwargs['image'].format(kwargs)
            entity = parent._replace(**kwargs)
            entity.__call__ = partial(_Entity, **_Entity._asdict())
            return entity
        return wrapped
    return decorator


@entity()
def Floor(walkable=True, image="floor-{texture}-{color}.png"):
    """Abstract walkable entity."""
