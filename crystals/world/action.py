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


class ActionSequence(Action):
    """Executes multiple actions "at once", one after the other in a given
    sequence.
    """

    def __init__(self, *actions):
        self.actions = actions

    def __call__(self, entity, *allargs):
        for action, args in zip(self.actions, allargs):
            action(entity, *args)


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
            entity, args = (yield)
            action(entity, *args)

        while True:
            entity, args = (yield)
            self.actions[-1](entity, *args)

    def __call__(self, entity, *args):
        self._iter.send((entity, args))


class UpdatePlot(Action):
    """Sends a given object to a given generator."""

    def __init__(self, updates):
        self.updates = updates

    def __call__(self, entity, plt):
        plt.send(self.updates)


class Alert(Action):
    """Writes given text to a given output stream."""
    
    def __init__(self, text):
        self.text = text

    def __call__(self, entity, output):
        output.write(self.text)


class Talk(Action):
    """Writes given text to a given output stream, prepended by the name
    of the acting entity.
    """

    sep = ': '

    def __init__(self, text):
        self.text = text

    def __call__(self, entity, output):
        output.write(entity.name + self.sep + self.text)
    

class Move(Action):
    pass
