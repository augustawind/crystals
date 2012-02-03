from nose.tools import raises

from crystals import *
from test.util import *


def _DummyEntity():
    return entity.Entity('', False, load_image('sack.png'), None)


class _OutputStream(object):
    """Dummy output stream."""

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class TestAction(object):
    
    def TestInit(self):
        nactions = 3
        action = world.action.Action(nactions)

    def TestExecute_NActionsPositive_DecrementNActions(self):
        nactions = 3
        action = world.action.Action(nactions)
        entity_ = _DummyEntity()
        for i in reversed(range(nactions)):

            action.execute(entity_)
            assert action.nactions == i

    def TestExecute_NActionsZero_DoNothing(self):
        entity_ = _DummyEntity()
        action = world.action.Action(0)

        action.execute(entity_)
        assert action.nactions == 0


class TestAlert(object):

    def TestInit(self):
        nactions = 3
        text = 'Hello, world!'
        output = _OutputStream()
        alert = world.action.Alert(nactions, text, output)

    def TestExecute_ValidOutputStream_WriteToOutput(self):
        nactions = 1
        text = 'whoa!'
        output = _OutputStream()
        alert = world.action.Alert(nactions, text, output)
        entity_ = _DummyEntity()

        alert.execute(entity_)
        assert output.last == text
