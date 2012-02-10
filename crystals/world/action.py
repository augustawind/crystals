"""actions that entities commit"""
import abc


class Action(object):
    """Abstract action that can be committed by an entity in the world."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        """Initialize the action, given its arguments."""

    @abc.abstractmethod
    def __call__(self, entity, *args):
        """Execute the action, given the entity responsible for it.
        
        Additional positional arguments are possible, but these must be
        registered with the game by adding an entry to 
        game.WorldMode.action_args for each subclass of Action that
        does so.
        """


class UpdatePlot(Action):
    """Action which updates a dictionary."""

    def __init__(self, updates):
        Action.__init__(self)
        self.updates = updates

    def __call__(self, entity, plot):
        """Update dict `plot` with self.updates."""
        Action.__call__(self, entity)
        plot.update(self.updates)


class Alert(Action):
    """Action which writes given text to a given output stream."""
    
    def __init__(self, text):
        Action.__init__(self)
        self.text = text

    def __call__(self, entity, output):
        """Write the text to the given output stream."""
        Action.__call__(self, entity)
        output.write(self.text)


class Talk(Alert):
    """Action which writes given text to a given output stream,
    prepended by the name of the acting entity.
    """

    sep = ': '

    def __init__(self, text):
        Alert.__init__(self, text)

    def __call__(self, entity, output):
        """Write the text to the given output stream, prepended by the
        entity's name plus class attribute `sep`.
        """
        Action.__call__(self, entity)
        output.write(entity.name + self.sep + self.text)
    

class Move(Action):
    pass
