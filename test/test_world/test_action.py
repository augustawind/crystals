import os
import sys

import pyglet
from nose.tools import raises

from crystals import world
from crystals.world import action
from test.util import *


class DummyAction(action.Action):

    def __init__(self):
        self.value = 0

    def __call__(self, entity):
        self.value = 1


def mockplot(triggers):
    while True:
        yield


@raises(TypeError)
def TestAction_IsAbstract():
    act = action.Action()


def TestActionIter():
    action1 = DummyAction()
    action2 = DummyAction()
    actioniter = action.ActionIter(action1, action2)

    actioniter(None)
    assert action1.value == 1
    assert action2.value == 0
    actioniter(None)
    assert action2.value == 1
    assert action1.value == 1


def TestActionSequence():
    action1 = DummyAction()
    action2 = DummyAction()
    actseq = action.ActionSequence(action1, action2)

    actseq(None, (), ())
    assert action1.value == 1
    assert action2.value == 1


class TestUpdatePlot(object):

    def TestInit(self):
        updates = {'foo': 'bar'}
        updateplot = action.UpdatePlot(updates)

    def TestCall_ValidPlotGiven_UpdatePlot(self):
        updates = ('foo', 'bar')
        updateplot = action.UpdatePlot(updates)
        plt = mockplot({})
        plt.next()
        updateplot(_DummyEntity(), plt)


class _OutputStream(object):
    """Dummy output stream."""

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class TestAlert(object):

    def TestInit(self):
        text = 'Hello, world!'
        alert = action.Alert(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'whoa!'
        alert = action.Alert(text)
        entity_ = None
        output = _OutputStream()
        alert(entity_, output)

        assert output.last == text


def _DummyEntity():
    return world.Entity('', False, 'sack.png', None)


class TestTalk(object):

    def TestInit(self):
        text = 'Yo, man'
        talk = action.Talk(text)

    def TestCall_ValidOutputStream_WriteToOutput(self):
        text = 'Yo, man'
        talk = action.Talk(text)

        entity_ = _DummyEntity()
        output = _OutputStream()
        talk(entity_, output)
        assert output.last == entity_.name + talk.sep + text
