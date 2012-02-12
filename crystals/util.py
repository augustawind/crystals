"""general-purpose utility functions"""


def coroutine(func):
    """A wrapper for generator functions that makes them act like coroutines.

    Return a function that acts like generator function `func` with
    the given args, but intercepts the returned generator and calls its
    `next` method before returning it to the caller.

    `Source <http://www.dabeaz.com/coroutines/coroutine.py>`_
    """
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start
