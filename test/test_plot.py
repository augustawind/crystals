from functools import partial

from crystals import plot


class TestPlot(object):

    def TestInit(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'PlayerCoords': (5, 5)}
        triggers = (
            ((lambda x: x), {'TalkedToDad': True}),
            ((lambda x: x), {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            ((lambda x: x), {'TalkedToDad': False, 'PlayerCoords': (3, 2)}))
        plt = plot.Plot(state, *triggers)

    def TestAddTriggers(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'PlayerCoords': (5, 5)}
        triggers = (
            ((lambda x: x), {'TalkedToDad': True}))
        plt = plot.Plot(state, triggers)

        plt.add_triggers(
            ((lambda x: x), {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            ((lambda x: x), {'TalkedToDad': False, 'PlayerCoords': (3, 2)}))

    def TestUpdate(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'PlayerCoords': (5, 5)}
        self.dummyvar = -1
        def setdummy(x):
            self.dummyvar = x
        triggers = (
            (partial(setdummy, 0), {'TalkedToDad': True}),
            (partial(setdummy, 1),
                {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            (partial(setdummy, 2),
                {'TalkedToDad': False, 'PlayerCoords': (3, 2)}))
        plt = plot.Plot(state, *triggers)

        plt.update({'TalkedToDad': True})
        assert self.dummyvar is 0
        plt.update({'#TimesCheckedBookcase': 3})
        assert self.dummyvar is 1
        plt.update({'PlayerCoords': (3, 2)})
        assert self.dummyvar is 1
        plt.update({'TalkedToDad': False})
        assert self.dummyvar is 2

        del self.dummyvar
