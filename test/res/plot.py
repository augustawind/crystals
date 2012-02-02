"""sample plot.py file"""

#from crystals.plot import Event

state = (
    CheckedBookcase(False),
    TalkedToDad(False),
    HadFirstFight(False),
    ObtainedHiddenScroll(False),
    ArrivedAtTemple(False),
    ...
    )


class CheckedBookcase(Event):

    def __init__(self, state, objects):
#        Event.__init__(self, state, objects)
        self.objects['bookcase'].checked = False

    def condition_met(self):
        return self.objects['bookcase'].checked == True
    
