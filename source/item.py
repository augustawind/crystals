"""item.py"""
from world import Entity

INF_USES = 0
MAX_USES = 99

class Item(Entity):
    
    def __init__(self, name, max_uses):
        self.name = name
        self.uses = max_uses
        self.max_uses = max_uses
    
    def __str__(self):
        return 'Item'
    
    def use(self):
        if self.uses < 1:
            return False
        self.uses -= 1
        return True
    
    def recharge(self):
        self.uses = self.max_uses
