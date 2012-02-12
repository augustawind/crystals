from functools import partial

from crystals import plot


class TestOldplot():

    def TestEverything(self):
        self.dummy = -1
        def setdummy(app, x):
            self.dummy = x

        func1, func2, func3 = (partial(setdummy, x=x) for x in range(3))
        plt = plot.plot({
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
        except plot.GameOver:
            assert self.dummy == 2
        else:
            assert False
        assert self.dummy is 2
