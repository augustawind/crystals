from random import randint
from itertools import repeat

def push_player(wmode):
    xstep, ystep = wmode.player.facing
    wmode.step_player(xstep * -1, ystep * -1)

TRIGGERS = {
    ('CheckTroll',): (push_player, {})}
