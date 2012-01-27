from nose.tools import raises

from crystals import *
from test.helpers import *

class TestAction(object):
    
    def test_init(self):
        nactions = 3
        action = interaction.Action(nactions)

    def test_execute(self):
        nactions = 3
        action = interaction.Action(nactions)
        entity_ = entity.Entity('', '', False, dummy_image, None)

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
        alert = interaction.Alert(nactions, text)
