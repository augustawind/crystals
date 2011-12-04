"""interaction between the player and other world entities"""

import abc 

class Interaction(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, count, order, sequence):
        self._count = count
        self._order = order
        self._sequence = sequence

        self._counter = 0

    @abc.abstractmethod
    def __str__(self):
        return 'Interaction'

    @property
    def order(self):
        return self._order

    @property
    def sequence(self):
        return self._sequence

    @abc.abstractmethod
    def interact(self):
        if self._counter < self._order:
            self._counter += 1
            return False
        elif self._count == -1:
            return True
        elif not self._count > 0:
            return False
        else:
            self._count -= 1
            return True

class TextInteraction(Interaction):
    """Outputs text on interact. Could be used for "dialog" with characters,
    reading signs, checking the environment, etc."""

    def __init__(self, count, order, sequence, text):
        super(TextInteraction, self).__init__(count, order, sequence)

        self.text = text

    def __str__(self):
        return 'text'

    def interact(self, output):
        if super(TextInteraction, self).interact():
            output.print_message(self.text)

class TalkInteraction(Interaction):
    """Outputs text preceded by the speaker's name, e.g. bob: hey!"""

    def __init__(self, count, order, text, speaker):
        super(TalkInteraction, self).__init__(count, order, sequence,
            speaker.name + ': ' + text)
