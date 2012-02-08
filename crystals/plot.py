"""tracking and responding to the game state"""


class Plot(object):
    """An object that stewards a state dictionary, triggering functions 
    when the state is modified in given ways.
    """

    def __init__(self, state, *triggers):
        self._state = state
        self._funcs = []
        self._conds = []
        self.add_triggers(*triggers)

    def add_triggers(self, *triggers):
        """Add function triggers to be called when their given state
        conditions are met.
        """
        for func, conds in triggers:
            self._funcs.append(func)
            self._conds.append(conds)
            

    def update(self, state):
        """Update the state dictionary and trigger any relevant events."""
        self._state.update(state)
        for cond in state:
            for (i, conds) in enumerate(self._conds):
                for c in conds:
                    print c
                if cond in conds and all(
                        self._state[c] == conds[c] for c in conds):
                    self._conds.pop(i)
                    self._funcs.pop(i)()
                    
