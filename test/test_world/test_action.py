from nose.tools import raises

from crystals import *
from test.util import *
from test.test_resource import imgloader

images = imgloader()

def _DummyEntity():
    return entity.Entity('', False, images.image('sack.png'), None)


class _OutputStream(object):
    """Dummy output stream."""

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class TestAction(object):
    
    def TestInit(self):
        count = 3
        action = world.action.Action(count)

    def TestExecute_countPositive_Decrementcount(self):
        count = 3
        action = world.action.Action(count)
        entity_ = _DummyEntity()
        for i in reversed(range(count)):

            action.execute(entity_)
            assert action.count == i

    def TestExecute_countZero_DoNothing(self):
        entity_ = _DummyEntity()
        action = world.action.Action(0)

        action.execute(entity_)
        assert action.count == 0


class TestAlert(object):

    def TestInit(self):
        count = 3
        text = 'Hello, world!'
        output = _OutputStream()
        alert = world.action.Alert(count, text, output)

    def TestExecute_ValidOutputStream_WriteToOutput(self):
        count = 1
        text = 'whoa!'
        output = _OutputStream()
        alert = world.action.Alert(count, text, output)
        entity_ = _DummyEntity()

        alert.execute(entity_)
        assert output.last == text
