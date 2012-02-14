import abc
from itertools import repeat, chain, cycle


class Action(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, wmode, entity):
        """Execute the action, given WorldMode object `wmode` and
        acting Entity object `entity`.
        """


class ActionIter(Action):
    def __init__(self, *actions):
        self.actions = iter(actions)
    def __call__(self, wmode, entity):
        try:
            action = next(self.actions)
        except StopIteration:
            pass
        else:
            action(wmode, entity)

class ActionCycle(ActionIter):
    def __init__(self, n, *actions):
        if n > 0:
            self.actions = chain(*repeat(actions, n))
        else:
            self.actions = cycle(actions)

class ActionSequence(Action):
    def __init__(self, *actions):
        self.actions = actions
    def __call__(self, wmode, entity):
        for action in self.actions:
            action(wmode, entity)

class NewAction(Action):
    def __init__(self, action):
        self.action = action
    def __call__(self, wmode, entity):
        entity.action = self.action
        self.action(wmode, entity)

class UpdatePlot(Action):
    def __init__(self, updates):
        self.updates = updates
    def __call__(self, wmode, entity):
        wmode.plot.send(self.updates)

class Alert(Action):
    def __init__(self, text):
        self.text = text
    def __call__(self, wmode, entity):
        wmode.infobox.write(self.text)

class Talk(Action):
    def __init__(self, text):
        self.text = text
    def __call__(self, wmode, entity):
        wmode.infobox.write(self.text)

class Move(Action):
    def __init__(self, xstep, ystep):
        self.step = (xstep, ystep)
    def __call__(self, wmode, entity):
        wmode.world.step_entity(entity, *self.step)


troll_action = ActionCycle(0,
    Talk('I like shorts.'),
    ActionSequence(
        UpdatePlot('CheckTroll'),
        Talk("Don't you, punk?!")),
    NewAction(Talk('I like shorts.')))
