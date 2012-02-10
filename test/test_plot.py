from functools import partial

from crystals import plot


class TestPlot(object):

    def TestInit(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'ACondition': 'foo'}
        triggers = (
            ((lambda: 1), {'TalkedToDad': True}),
            ((lambda: 1), {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            ((lambda: 1), {'TalkedToDad': False, 'ACondition': 'bar'}))
        plt = plot.Plot(state, *triggers)

    def TestAddTriggers(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'ACondition': 'foo'}
        triggers = ((lambda: 1), {'TalkedToDad': True})
        plt = plot.Plot(state, triggers)
        assert len(plt.triggers) == 1
        assert plt.triggers[0] == triggers

        new_triggers = [
            ((lambda: 1), {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            ((lambda: 1), {'TalkedToDad': False, 'ACondition': 'bar'})]
        plt.add_triggers(*new_triggers)
        assert len(plt.triggers) is 3
        assert plt.triggers[1:] == new_triggers

    def TestSetItem(self):
        state = {
            'TalkedToDad': False,
            '#TimesCheckedBookcase': 1,
            'ACondition': 'foo'}
        self.dummyvar = -1
        def setdummy(x):
            self.dummyvar = x
        triggers = (
            (partial(setdummy, 0), {'TalkedToDad': True}),
            (partial(setdummy, 1),
                {'TalkedToDad': True, '#TimesCheckedBookcase': 3}),
            (partial(setdummy, 2),
                {'TalkedToDad': False, 'ACondition': 'bar'}))
        plt = plot.Plot(state, *triggers)

        plt['NewDictItem'] = 333
        assert self.dummyvar is -1
        plt['TalkedToDad'] = True
        assert self.dummyvar is 0
        plt['#TimesCheckedBookcase'] = 3
        assert self.dummyvar is 1
        plt['ACondition'] = 'bar'
        assert self.dummyvar is 1
        plt['TalkedToDad'] = False
        assert self.dummyvar is 2

        del self.dummyvar

    def TestUpdate(self):
        state = {'foo': 0, 'bar': 1, 'baz': 2}
        trigger = (partial(state.__setitem__, 'baz', 'foobar'),
                   {'foo': 1, 'bar': 2})
        plt = plot.Plot(state, trigger)

        plt.update({'foo': 1, 'bar': 2})
        assert state['baz'] == 'foobar'
