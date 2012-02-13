"""the component parts of a world"""
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


class ActionIter(Action):
    """Executes actions in a sequence, executing the next action each
    time the ActionIter instance is called.

    Each call after all actions are exhausted will call the last action
    in the sequence.
    """

    def __init__(self, *actions):
        self.actions = actions
        self._iter = self._iter_actions()
        next(self._iter)

    def _iter_actions(self):
        for action in self.actions:
            args = (yield)
            action(*args)

        while True:
            args = (yield)
            self.actions[-1](*args)

    def __call__(self, *args):
        self._iter.send(args)


class UpdatePlot(Action):
    """Action which updates a Plot instance."""

    def __init__(self, updates):
        self.updates = updates

    def __call__(self, entity, plt):
        """Send plot generator `plt` self.updates."""
        plt.send(self.updates)


class Alert(Action):
    """Action which writes given text to a given output stream."""
    
    def __init__(self, text):
        self.text = text

    def __call__(self, entity, output):
        """Write the text to the given output stream."""
        output.write(self.text)


class Talk(Action):
    """Action which writes given text to a given output stream,
    prepended by the name of the acting entity.
    """

    sep = ': '

    def __init__(self, text):
        self.text = text

    def __call__(self, entity, output):
        """Write the text to the given output stream, prepended by the
        entity's name plus class attribute `sep`.
        """
        output.write(entity.name + self.sep + self.text)
    

class Move(Action):
    pass
