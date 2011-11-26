"""interaction.py"""

class Interactable(object):

    def __init__(self, count):
        self.count = count

    def interact(self):
        if self.count == -1:
            return True
        if not self.count > 0:
            return False
        self.count -= 1
        return True

class TextInteractable(Interactable):
    """Outputs text on interact. Could be used for "dialog" with characters,
    reading signs, checking the environment, etc."""

    def __init__(self, count, text):
        super(TextInteractable, self).__init__(count)

        self.text = text

    def __str__(self):
        return 'TextInteractable'

    def interact(self, output):
        if super(TextInteractable, self).interact():
            output.print_message(self.text)
