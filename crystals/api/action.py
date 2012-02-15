"""helpers aid in writing world and plot scripts"""

import abc
from itertools import *


class Action(object):
    """Abstract entity action class.
    
    All entity action classes should derive from this class.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, wmode, entity):
        """Execute the action, given WorldMode object `wmode` and
        acting Entity object `entity`.

        :param wmode: the active WorldMode object
        :type wmode: crystals.app.Worldmode
        :param entity: the "acting" entity
        :type entity: crystals.world.Entity
        """


class ActionIter(Action):
    """On call, calls the next action in sequence.
    
    Once the end of the sequence has been reached, each call to
    ActionIter calls the final action in the sequence.
    """

    def __init__(self, *actions):
        assert actions
        self.actions = chain(actions[:-1], repeat(actions[-1]))

    def __call__(self, wmode, entity):
        next(self.actions)(wmode, entity)


class ActionLoop(ActionIter):
    """On call, calls the next action in sequence, starting over at the
    beginning once the end of the sequence is reached.
    """

    def __init__(self, *actions):
        assert actions
        self.actions = cycle(actions)


class ActionCycle(Action):
    """On call, acts like ActionIter, but iterates through the action
    sequence N times before resting on the final action.
    """

    def __init__(self, n, *actions):
        """Initialize the action. 

        :param n: number of times to repeat the sequence 
        :type n: int > 1
        :param actions: one or more action objects
        """
        assert type(n) is int and n > 1
        assert actions
        self.actions = chain(*repeat(actions, n))
        self._final_action = actions[-1]

    def __call__(self, wmode, entity):
        try:
            action = next(self.actions)
        except StopIteration:
            self.actions = repeat(self._final_action)
            action = next(self.actions)
        finally:
            action(wmode, entity)


class ActionSequence(Action):
    """On call, calls each given action in sequence."""

    def __init__(self, *actions):
        self.actions = actions

    def __call__(self, wmode, entity):
        for action in self.actions:
            action(wmode, entity)


class ResetAction(Action):
    """On call, overwrites the entity's action with the given action."""

    def __init__(self, action):
        self.action = action

    def __call__(self, wmode, entity):
        entity.action = self.action
        self.action(wmode, entity)


class UpdatePlot(Action):
    """On call, sends updates to the plot generator."""

    def __init__(self, updates):
        self.updates = updates

    def __call__(self, wmode, entity):
        wmode.plot.send(self.updates)


class Alert(Action):
    """On call, writes text to the infobox."""

    def __init__(self, text):
        self.text = text

    def __call__(self, wmode, entity):
        wmode.infobox.write(self.text)


class Talk(Action):
    """On call, writes text to the infobox preceded by the name of the
    speaking entity.
    """

    def __init__(self, text):
        self.text = text

    def __call__(self, wmode, entity):
        wmode.infobox.write(self.text)


class Move(Action):
    """On call, move the entity a given distance from its current location."""

    def __init__(self, xstep, ystep):
        """Initialize the action.

        :param xstep: number of tiles to move horizontally
        :type xstep: int
        :param ystep: number of tiles to move vertically
        :type ystep: int
        """
        self.step = (xstep, ystep)

    def __call__(self, wmode, entity):
        wmode.world.step_entity(entity, *self.step)

