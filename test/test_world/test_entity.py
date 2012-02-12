import os
import sys

import pyglet
from nose.tools import raises

from crystals import *
from crystals.world import entity
from test.util import *


def TestEntity():
    entity_ = entity.Entity('an entity', True, 'sack.png', facing=(0, 1),
                            actions=[])


@raises(TypeError)
def TestAction_IsAbstract(object):
    action = entity.Action()


class TestUpdatePlot(object):

    def TestInit(self):
        updates = {'foo': 'bar'}
        updateplot = entity.UpdatePlot(updates)

    def TestCall_ValidPlotGiven_UpdatePlot(self):
        updates = {'foo': 'bar'}
        updateplot = entity.UpdatePlot(updates)
        plt = {'foo': 'baz', 'bip': 'bop'}
        updateplot(_DummyEntity(), plt)
        plt['foo'] == 'bar'
        assert plt['bip'] == 'bop'


class _OutputStream(object):
    """Dummy output stream."""

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class TestAlert(object):

    def TestInit(self):
        text = 'Hello, world!'
        alert = entity.Alert(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'whoa!'
        alert = entity.Alert(text)
        entity_ = None
        output = _OutputStream()
        alert(entity_, output)

        assert output.last == text


def _DummyEntity():
    return world.Entity('', False, 'sack.png', None)


class TestTalk(object):

    def TestInit(self):
        text = 'Yo, man'
        talk = entity.Talk(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'Yo, man'
        talk = entity.Talk(text)

        entity_ = _DummyEntity()
        output = _OutputStream()
        talk(entity_, output)
        assert output.last == entity_.name + talk.sep + text

