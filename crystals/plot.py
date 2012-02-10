"""tracking and responding to the game state"""


class Plot(dict):
    """A dict that executes given functions when its items have
    given values.
    """

    def __init__(self, state, *triggers):
        dict.__init__(self, state)
        self._funcs = []
        self._conds = []
        self.add_triggers(*triggers)

    def _trigger_key(self, key):
        for (i, conds) in enumerate(self._conds):
            if key in conds and all(self[c] == conds[c] for c in conds):
                self._conds.pop(i)
                self._funcs.pop(i)()
            
    def __setitem__(self, key, val):
        """Call dict.__setitem__ on self, then trigger any relevant events."""
        dict.__setitem__(self, key, val)
        if key not in self:
            return
        self._trigger_key(key)

    def update(self, other):
        """Call dict.update on self, then trigger any relevant events."""
        dict.update(self, other)

        for key in dict(other):
            self._trigger_key(key)

    @property
    def triggers(self):
        return zip(self._funcs, self._conds)

    def add_triggers(self, *triggers):
        """Add function triggers to be called when their given state
        conditions are met.
        """
        for func, conds in triggers:
            self._funcs.append(func)
            self._conds.append(conds)
                    
