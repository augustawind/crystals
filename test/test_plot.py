from functools import partial
from collections import namedtuple

from crystals import plot


class TestNewPlot():

    def __init__(self):
        self.dummy = -1
        def setdummy(self, app, x):
            self.dummy = x

        func1, func2, func3 = (partial(setdummy, x=x) for x in range(3))
        plt = plot.Plot({
            ('State1', 'State2'): (func1, {
                ('State3',): (func2, {}),
                ('State4',): (func3, {})
            })
        })
        assert plt.triggers == {
            frozenset(('State1', 'State2')): (func1, {
                frozenset(('State3',)): (func2, {}),
                frozenset(('State4',)): (func3, {})
            })
        }

        newset = set((1, 2, 3))
        plt.update(*newset)
        assert not (plt.state ^ newset)
        assert self.dummy is -1

        plt.update('State1', 'State2')
        assert self.dummy is 0
        plt.update('State3')
        assert self.dummy is 0
        plt.update('State5')
        assert self.dummy is 0
        assert self.dummy is 0
