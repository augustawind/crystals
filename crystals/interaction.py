"""interaction between the player and other world entities"""

import abc 

class Interaction(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, count, order):
        self._count = count
        self._order = order

    @abc.abstractmethod
    def __str__(self):
        return 'Interaction'

    @property
    def order(self):
        return self._order

    @abc.abstractmethod
    def interact(self):
        if self._count == -1:
            return True
        if not self._count > 0:
            return False
        self._count -= 1
        return True

class TextInteraction(Interaction):
    """Outputs text on interact. Could be used for "dialog" with characters,
    reading signs, checking the environment, etc."""

    def __init__(self, count, order, text):
        super(TextInteraction, self).__init__(count, order)

        self.text = text

    def __str__(self):
        return 'text'

    def interact(self, output):
        if super(TextInteraction, self).interact():
            output.print_message(self.text)
