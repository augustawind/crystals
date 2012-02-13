STATE = ()

# trigger functions
# ----------------------------------------------------------------------
def troll_push_player(wmode):
    xstep, ystep = wmode.player.facing
    xstep *= -1
    ystep *= -1
    wmode.step_player(xstep, ystep)
    wmode.world.step_entity('troll', xstep, ystep)
# ----------------------------------------------------------------------


TRIGGERS = {
    ('CheckTroll',): (troll_push_player, {
        ('TranscendSpaceAndTime',): (lambda: 1 / 0, {})
        })
    }
