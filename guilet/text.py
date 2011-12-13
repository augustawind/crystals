import pyglet

from guilet.base import Widget
from guilet import color

class TextBox(Widget):
    """A box that displays text."""

    def __init__(self, x, y, width, height, batch, padding=0,
                 text_args={'font-size': 12, 'color': color.DEFAULT)},
                 *args, **kwargs):
        super(TextBox, self).__init__(x, y, width, height, batch,
                                      *args, **kwargs)
        self.padding = padding
        self.document = pyglet.text.decode_text('')
        self.layout = IncrementalTextLayout(
            self.document,
            self.width - (padding * 2), self.height - (padding * 2),
            multiline=True, batch=self.batch, group=self.group)

    def set_style(self, style):
        self.document.set_style(0, len(self.document.text), style)

    def append_text(self, text):
        """Append text to the text box."""
        self.document.insert_text(len(self.document.text), text)

    def insert_text(self, text, i=0):
        """Insert text into the text box."""
        self.document.insert_text(i, text)

    def delete_text(self, start, end):
        """Delete a section of text from the text box."""
        self.document.delete_text(start, end)

    def clear(self):
        """Delete all text from the text box."""
        self.document.text = ''

    def update(self):
        super(TextBox, self).update()
        self.layout.x = self.x + self.padding
        self.layout.y = self.y + self.padding
        self.layout.width = self.width - (padding * 2)
        self.layout.height = self.height - (padding * 2)

        self.content_width = self.layout.content_width
        self.content_height = self.layout.content_height


class TextFeed(TextBox):
    """A text box that prints messages preceded by bullet points,
    in a scrolling pane."""

    def __init__(self, x, y, width, height, batch, bullet='>>',
                 *args, **kwargs):
        super(TextFeed, self).__init__(x, y, width, height, batch,
                                       *args, **kwargs)
        self.bullet = bullet

    def _format(self, text):
        return '\n' + self.bullet + text

    def write(self, text):
        super(TextFeed, self).append(self._format(text))
        self.layout.ensure_line_visible(-1)
