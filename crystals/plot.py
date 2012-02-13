"""implementation of plot mechanics, the higher powers driving the game"""
from crystals.util import coroutine


class GameOver(BaseException):
    """Raised when the game is over."""


def _format_triggers(triggers):
    return dict((frozenset(k), (v[0], _format_triggers(v[1])))
                for k, v in triggers.iteritems())


@coroutine
def plot(state, triggers):
    """Return a plot generator, given an initial state set and a
    mapping of functions to potential state elements.

    `triggers` must be a dictionary where each key is an arbitrary-
    length tuple of unique plot state identifiers, and each value is
    a 2-tuple where the first item is a callable to be called when
    the plot states given in the key exist, and the second item is
    either an empty dict or a nested `triggers` dict::

        plt = plot({
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

    For each trigger at the top level whose conditions have been met,
    the corresp. function is called with the controlling application
    as its sole argument. That entry is then deleted except for nested
    entries, which are moved up a level. Once the triggers are exhausted,
    GameOver is raised.
    """
    triggers = _format_triggers(triggers)

    app = (yield)
    assert app

    while triggers:
        # Get state updates
        updates = (yield)
        if updates is None:
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

    raise GameOver()
