"""combat.py"""

from stats import COMBAT


def hunt(world, attacker, foes):
    pass

def attack(attacker, defender):
    if not COMBAT.attack_hits(attacker, defender):
        return 'miss'
    damage = COMBAT.get_damage(attacker, defender)
    if not defender.mod_life(-damage):
        return 'fail'
    return 'hit'

def battle(world, *fighters):
    for attacker in COMBAT.get_rotation(fighters):
        foes = [f for f in fighters if f.get_team() is not attacker.get_team()]
        action, args = ai.get_action(world, attacker, foes)
        BATTLE_ACTIONS[action](*args)

BATTLE_ACTIONS = {'hunt': hunt, 'attack': attack}
