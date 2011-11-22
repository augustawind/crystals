from random import random

def get_rotation(self, *characters):
    """Return characters list sorted by agl stat, highest to lowest."""
    return sorted(characters,
        key=lambda x: x.get_attr('agl' + random(), reverse=True))

def get_damage(self, attacker, defender):
    """Return damage dealt to defender in an attack from attacker."""
    return attacker.get_attr('str') - (defender.get_attr('end') / 2)

def attack_hits(self, attacker, defender):
    """Return True if attack by attacker hits defender."""
    return ((attacker.get_attr('dex') - defender.get_attr('dex') + 75) / 100.0 >
             random())
