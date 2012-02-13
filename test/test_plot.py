from functools import partial

from crystals import plot


class TestPlot():

    def TestEverything(self):
        self.dummy = -1
        def setdummy(app, x):
            self.dummy = x

        state = set()
        func1, func2, func3 = (partial(setdummy, x=x) for x in range(3))
        plt = plot.plot(
            state,
            {('State1', 'State2'): (func1, {
                ('State3',): (func2, {}),
                ('State4',): (func3, {})
            })
        })

        app = object()
        plt.send(app)
        assert self.dummy == -1
        assert len(state) == 0

        plt.send(('State1', 'State2'))
        assert self.dummy == 0
        assert len(state) == 2
        plt.send('State3')
        assert self.dummy == 1
        assert len(state) == 3
        plt.send('State5')
        assert self.dummy == 1
        assert len(state) == 4

        try:
            plt.send('State4')
        except plot.GameOver:
            assert self.dummy == 2
            assert len(state) == 5
        else:
            assert False
        assert self.dummy is 2
