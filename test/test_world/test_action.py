from nose.tools import raises

from crystals import *
from test.util import *


def dummy_entity():
    return entity.Entity('', '', False, dummy_image, None)


class Output(object):

    def __init__(self):
        self.text = ''

    def write(self, text):
        self.last = text


class ConcreteAction(world.action.Action):

    def execute(self, entity):
        world.action.Action.execute(self, entity)


class TestAction(object):
    
    def test_init(self):
        nactions = 3
        action = ConcreteAction(nactions)

    def test_execute(self):
        nactions = 3
        action = ConcreteAction(nactions)

        entity_ = dummy_entity()
        for i in reversed(range(nactions)):
            action.execute(entity_)
            assert action.nactions == i

        assert action.nactions == 0
        action.execute(entity_)
        assert action.nactions == 0


class TestAlert(object):

    def test_init(self):
        nactions = 3
        text = 'Hello, world!'
        output = Output()
        alert = world.action.Alert(nactions, text, output)

    def test_execute(self):
        nactions = 1
        text = 'whoa!'
        output = Output()
        alert = world.action.Alert(nactions, text, output)

        entity_ = dummy_entity()
        alert.execute(entity_)
        assert output.last == text
