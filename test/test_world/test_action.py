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


@raises(TypeError)
def TestAction_IsAbstract(object):
    action = world.action.Action()


class TestUpdatePlot(object):

    def TestInit(self):
        updates = {'foo': 'bar'}
        updateplot = world.action.UpdatePlot(updates)

    def TestCall_ValidPlotGiven_UpdatePlot(self):
        updates = {'foo': 'bar'}
        updateplot = world.action.UpdatePlot(updates)
        plt = {'foo': 'baz', 'bip': 'bop'}
        updateplot(_DummyEntity(), plt)
        plt['foo'] == 'bar'
        assert plt['bip'] == 'bop'


class TestAlert(object):

    def TestInit(self):
        text = 'Hello, world!'
        alert = world.action.Alert(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'whoa!'
        alert = world.action.Alert(text)
        entity_ = _DummyEntity()
        output = _OutputStream()
        alert(entity_, output)

        assert output.last == text


class TestTalk(object):

    def TestInit(self):
        text = 'Yo, man'
        talk = world.action.Talk(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'Yo, man'
        talk = world.action.Talk(text)

        entity_ = _DummyEntity()
        output = _OutputStream()
        talk(entity_, output)
        assert output.last == entity_.name + talk.sep + text
