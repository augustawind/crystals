"""actions that entities commit"""


class Action(object):
    """An action that can be committed by an entity in the world."""

    def __init__(self, nactions):
        self.nactions = nactions
    
    def execute(self, entity):
        """Execute the action, given the entity responsible for it."""
        if self.nactions < 1:
            return
        self.nactions -= 1


class Alert(Action):
    """Action which writes given text to a given output stream,
    presumably the game's infobox.
    """

    def __init__(self, nactions, text, output):
        Action.__init__(self, nactions)
        self.text = text
        self.output = output

    def execute(self, entity):
        """Write the text to the output stream."""
        Action.execute(self, entity)
        self.output.write(self.text)
