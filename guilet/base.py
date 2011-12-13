"""base classes for all gui components"""
import pyglet

from guilet import color

class Rectangle(object):
    """A rectangle that can be drawn into a batch."""

    def __init__(self, x1, y1, x2, y2, batch, group=None,
                 color=color.DEFAULT, filled=False, visible=True):
        self._color = color
        self._visible = False
        self._position_data = ('v2i', (x1, y1, x2, y1, x2, y2, x1, y2))
        self._color_data = ('c4B', color * 4)
        self._vertex_list = None

        self.batch = batch
        self.group = group
        self.filled = filled
        if visible:
            self.render()

    @property
    def color(self):
        return self._color

    @property
    def visible(self):
        return self._visible

    def render(self):
        """Add the vertices to the batch."""
        if self._visible:
            return
        if self.filled:
            self._vertex_list = self.batch.add(
                4, pyglet.gl.GL_QUADS, self.group,
                self._position_data, self._color_data)
        else:
            self._vertex_list = self.batch.add_indexed(
                4, pyglet.gl.GL_LINES, self.group,
                (0, 1, 0, 3, 1, 2, 2, 3),
                self._position_data, self._color_data)
        self._visible = True

    def delete(self):
        """Delete the vertices."""
        if not self._visible:
            return
        self._vertex_list.delete()
        self._visible = False


class Widget(object):
    """Base class for GUI elements."""

    def __init__(self, x, y, width, height, batch, group=None,
                 border_color=color.DEFAULT, bg_color=color.DEFAULT,
                 show_border=False, show_bg_color=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.batch = batch
        if group:
            self.group = group
        else:
            self.group = pyglet.graphics.OrderedGroup(1)

        self.border = None
        self.bg_color = None
        self.set_border(border_color, show_border)
        self.set_bg_color(bg_color, show_bg_color)
    
    def _get_offset_group(self, offset):
        return pyglet.graphics.OrderedGroup(self.group.order + offset)

    def _get_centered_coords(self, width, height):
        """Return (x, y) coordinates of the point at which a label or image
        with given width and height must be placed in order to be centered in
        the Widget."""
        x1, y1, x2, y2 = self.get_bounds()
        x = ((x2 + x1) / 2) - (width / 2)
        y = ((y2 + y1) / 2) - (height / 2)
        return x, y

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    position = property(get_position, set_position)

    def get_size(self):
        return self.width, self.height

    def set_size(self, size):
        self.width, self.height = size

    size = property(get_size, set_size)
    
    def get_bounds(self):
        """Return the Widget's edge coordinates as (x1, y1, x2, y2)."""
        return self.x, self.y, self.x + self.width, self.y + self.height

    def set_border(self, color, visible=True):
        """Sets a new border rectangle with given color and visibility."""
        if self.border is not None:
            self.border.delete()
        if color is None:
            return
        x1, y1, x2, y2 = self.get_bounds()
        self.border = Rectangle(
            x1, y1, x2, y2, self.batch, self.group, color, visible=visible)

    def set_bg_color(self, color, visible=True):
        """Sets a new background color rectangle with given color and
        visibility."""
        if self.bg_color is not None:
            self.bg_color.delete()
        if color is None:
            return
        x1, y1, x2, y2 = self.get_bounds()
        self.bg_color = Rectangle(
            x1, y1, x2, y2, self.batch, self._get_offset_group(-1), color,
            filled=True, visible=visible)

    def update(self):
        """Redraw everything to reflect current state of rendering properties.
        """
        self.set_border(self.border.color, self.border.visible)
        self.set_bg_color(self.bg_color.color, self.bg_color.visible)


class Label(Widget):
    """A Widget that can display text and an image."""

    def __init__(self, x, y, width, height, batch, text=None, image=None,
                 text_args={'font_size': 12, 'color': color.DEFAULT},
                 image_args={'scale': 1, 'rotation': 0},
                 *args, **kwargs):
        super(Label, self).__init__(x, y, width, height, batch,
                                            *args, **kwargs)

        self._label = pyglet.text.Label(
            "", x=0, y=0, width=self.width, height=None, halign='center',
            multiline=False, anchor_x='left', anchor_y='bottom',
            batch=self.batch, group=self._get_offset_group(1), **text_args)
        if text:
            self.set_text(text, **text_args)
        self._sprite = None
        if image:
            self.set_image(image, **image_args)

    def set_text(self, text, **style):
        """Change the text on the label, then update the label's position."""
        self._label.text = text
        for name, value in style.iteritems():
            self._label.set_style(name, value)
        self._label.x, self._label.y = self._get_centered_coords(
            self._label.content_width, self._label.content_height)

    def set_image(self, image, scale=1, rotation=0):
        """Sets a new Sprite with given image, scale, and rotation."""
        if self._sprite:
            self._sprite.delete()
        if image is None:
            self._sprite = None
            return

        if self._sprite is None:
            x, y = self._get_centered_coords(
                image.width, image.height)
            self._sprite = pyglet.sprite.Sprite(
                image, x, y, batch=self.batch, group=self.group)
        else:
            self._sprite.image = image
        self.sprite.scale = scale
        self.sprite.rotation = rotation
        self.bg_color.hide()

    def update(self):
        super(Label, self).update()
        self.set_text(self._label.text)
        self.set_image(self._sprite.image if self._sprite else None)


class Panel(Widget):
    """A Widget that contains other Widgets."""

    def __init__(self, x, y, width, height, batch, *args, **kwargs):
        super(Panel, self).__init__(x, y, width, height, batch,
                                    *args, **kwargs)
        self.widgets = []

    def _init_widget(self, widget, x=None, y=None):
        if x is None:
            x = widget.x
        if y is None:
            y = widget.y
        widget.x = self.x + x
        widget.y = self.y + y
        widget.update()

    def add(self, widget, x=None, y=None):
        self.widgets.append(widget)
        self._init_widget(widget, x, y)

    def insert(self, widget, x=None, y=None, i=0):
        self.widgets.insert(widget, i)
        self._init_widget(widget, x, y)

    def remove(self, widget):
        self.widgets.remove(widget)

    def pop(self, i=-1):
        self.widgets.pop(i)
