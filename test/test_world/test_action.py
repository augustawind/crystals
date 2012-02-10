from nose.tools import raises

from crystals import *
from test.util import *
from test.test_resource import imgloader

images = imgloader()

def _DummyEntity():
    return world.Entity('', False, images.image('sack.png'), None)


class _OutputStream(object):
    """Dummy output stream."""

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class TestAction(object):
    
    def TestInit(self):
        action = world.action.Action()


class TestAlert(object):

    def TestInit(self):
        text = 'Hello, world!'
        alert = world.action.Alert(text)

    def TestExecute_ValidOutputStream_WriteToOutput(self):
        text = 'whoa!'
        alert = world.action.Alert(text)
        entity_ = _DummyEntity()
        output = _OutputStream()
        alert.execute(entity_, output)

        assert output.last == text


class TestUpdatePlot(object):

    def TestInit(self):
        updates = {'foo': 'bar'}
        updateplot = world.action.UpdatePlot(updates)

    def TestExecute(self):
        updates = {'foo': 'bar'}
        updateplot = world.action.UpdatePlot(updates)
        plt = {'foo': 'baz', 'bip': 'bop'}
        updateplot.execute(_DummyEntity(), plt)
        plt['foo'] == 'bar'
        assert plt['bip'] == 'bop'

