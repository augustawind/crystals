"""actions that entities commit"""


class Action(object):
    """Abstract action that can be committed by an entity in the world."""

    def __init__(self, *args, **kwargs):
        """Initialize the action, given its arguments."""

    def execute(self, entity):
        """Execute the action, given the entity responsible for it."""


class Alert(Action):
    """Action which writes given text to a given output stream,
    presumably the game's infobox.
    """
    
    def __init__(self, text):
        Action.__init__(self)
        self.text = text

    def execute(self, entity, output):
        """Write the text to the given output stream."""
        Action.execute(self, entity)
        output.write(self.text)


class UpdatePlot(Action):
    """Action which updates a dictionary."""

    def __init__(self, updates):
        Action.__init__(self)
        self.updates = updates

    def execute(self, entity, plot):
        """Update dict `plot` with self.updates."""
        Action.execute(self, entity)
        plot.update(self.updates)
