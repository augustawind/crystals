from functools import partial

from crystals import plot


class TestPlotGen():

    def TestEverything(self):
        self.dummy = -1
        def setdummy(app, x):
            self.dummy = x

        func1, func2, func3 = (partial(setdummy, x=x) for x in range(3))
        plt = plot.plotgen({
            ('State1', 'State2'): (func1, {
                ('State3',): (func2, {}),
                ('State4',): (func3, {})
            })
        })

        app = object()
        plt.send(app)
        assert self.dummy == -1

        plt.send(('State1', 'State2'))
        assert self.dummy == 0
        plt.send('State3')
        assert self.dummy == 1
        plt.send('State5')
        assert self.dummy == 1
        try:
            plt.send('State4')
        except StopIteration:
            assert self.dummy == 2
        else:
            assert False


class TestPlot():

    def TestEverything(self):
        self.dummy = -1
        def setdummy(app, x):
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
        assert self.dummy is 1
        plt.update('State5')
        assert self.dummy is 1
        plt.update('State4')
        assert self.dummy is 2
