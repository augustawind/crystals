"""keeping track of and responding to the game state"""

from crystals.util import coroutine


def _format_triggers(triggers):
    """Convenience function that returns a properly formatted
    trigger dict given a lazily formatted trigger dict.

    Apply builtin function `frozenset` recursively to the keys of
    `triggers` as well as the keys of all nested dicts.
    Accepted formats for `triggers` are described in the
    documentation for the constructor.
    """
    return dict((frozenset(k), (v[0], _format_triggers(v[1])))
                for k, v in triggers.iteritems())


@coroutine
def plotgen(triggers):
    """Return a plot generator, given dict `triggers` containing
    structured plot information.

    `triggers` must be a dictionary where each key is an arbitrary-
    length tuple of unique plot state identifiers, and each value is
    a 2-tuple where the first item is a callable to be called when
    the plot states given in the key exist, and the second item is
    either an empty dict or a nested `triggers` dict::

        plt = Plot({
            ('state1', 'state2'): (func1, {
                ('state3', ): (func2, {}),
                ('state4', ): (func3, {
                    ...}),
                ...}),
            ('state5',): (func4, {}),
            ...})

    After creating a generator, its first iteration should be to send it 
    the controlling application object. Thereafter, any calls to `send`
    are treated as plot updates, and the triggers are checked to see if
    their conditions have been met. Calls to `next` or `send(None)` are
    ignored.

    For each trigger at the top level whose condtions have been met,
    the corresp. function is called with the controlling application
    as its sole argument. That entry is then deleted except for nested
    entries, which are moved up a level. Once the triggers are exhausted,
    StopIteration is raised.
    """
    triggers = _format_triggers(triggers)
    state = set()

    app = (yield)
    assert app

    while triggers:
        # Get state updates
        updates = (yield)
        if not updates:
            continue

        # Update state
        if type(updates) in (tuple, set, frozenset, list):
            state.update(updates)
        else:
            state.add(updates)

        # Call trigger functions
        for req_state, (func, nextbranch) in triggers.items():
            if req_state <= state:
                func(app)
                del triggers[req_state]
                triggers.update(nextbranch)


class Plot(object):
    def __init__(self, triggers, app=None):
        """Return a plot instance, given dict `triggers` containing
        structured plot information.

        `triggers` must be a dictionary where each key is an arbitrary-
        length tuple of unique plot state identifiers, and each value is
        a 2-tuple where the first item is a callable to be called when
        the plot states given in the key exist, and the second item is
        either an empty dict or a nested `triggers` dict::

            plt = Plot({
                ('state1', 'state2'): (func1, {
                    ('state3', ): (func2, {}),
                    ('state4', ): (func3, {
                        ...}),
                    ...}),
                ('state5',): (func4, {}),
                ...})

        `app` is the controlling application of the plot, and is passed
        as the sole argument to each triggered function as they are
        respectively called. It may be omitted, but usually you'll want
        to assign something to it before calling `self.update`.
        """
        self._triggers = self._format_triggers(triggers)
        self._state = set()
        self._app = None

    def _format_triggers(self, triggers):
        """Convenience function that returns a properly formatted
        trigger dict given a lazily formatted trigger dict.

        Apply builtin function `frozenset` recursively to the keys of
        `triggers` as well as the keys of all nested dicts.
        Accepted formats for `triggers` are described in the
        documentation for the constructor.
        """
        return dict((frozenset(k), (v[0], self._format_triggers(v[1])))
                    for k, v in triggers.iteritems())

    def _get_app(self): return self._app
    def _set_app(self, app): self._app = app
    app = property(_get_app, _set_app,
        """The application controlling the plot.
        
        Triggered functions are passed this property as the sole
        argument.
        """)

    @property
    def state(self):
        """A set describing the current state of the plot."""
        return self._state

    @property
    def triggers(self):
        """A dict describing the plot's current state triggers."""
        return self._triggers

    def update(self, *elems):
        """Add elements to the plot state, causing any trigger functions
        to be called if their element requirements are now met.
        """
        self._state.update(elems)

        for req_state, (func, nextbranch) in self._triggers.items():
            if req_state <= self._state:
                func(self.app)
                del self._triggers[req_state]
                self._triggers.update(nextbranch)
