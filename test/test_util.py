from crystals import util


def TestCoroutine():

    @util.coroutine
    def gen_func(x, y=5):
        value = (yield)
        yield x + value, y + value

    x = 3
    y = 6
    gen = gen_func(x, y=y)
    n = 1
    x1, y1 = gen.send(n)
    assert x1 is x + n
    assert y1 is y + n
    
