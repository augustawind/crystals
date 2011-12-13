"""menus and menu items"""

import pyglet
from pyglet.window import key, mouse

from guilet.base import Label, Panel

class MenuItem(Label):
    """An label for an item in a menu. Calls a given function when triggered.
    """

    def __init__(self, x, y, width, height, batch, func=lambda x: None,
                 func_args=(), *args, **kwargs):
        super(MenuItem, self).__init__(x, y, width, height, batch,
                                         *args, **kwargs)
        self.func = func
        self.func_args = func_args
        self._selected = False

    @property
    def selected(self):
        return self._selected
        
    def hit_test(self, x, y):
        """Return True if `x` and `y` are within
        the menu item's x and y bounds.
        """
        x1, y1, x2, y2 = self.get_bounds()
        return x1 <= x <= x2 and y1 <= y <= y2

    def select(self):
        """Select the menu item, displaying a border around it."""
        if not self._selected:
            self.border.render()
            self._selected = True

    def deselect(self):
        """Deselect the menu item, hiding its border."""
        if self.selected:
            self.border.delete()
            self._selected = False

    def trigger(self):
        """Trigger the menu item, calling its trigger function property."""
        self.func(*self.func_args)


class MenuBranch(MenuItem):
    """A menu item that activates a submenu."""

    def __init__(self, x, y, width, height, batch, menu,
                 *args, **kwargs):
        self.menu = menu
        super(MenuBranch, self).__init__(
            x, y, width, height, batch, self.menu.activate,
            *args, **kwargs)


class Menu(Panel):
    """A panel of coordinated menu items."""

    def __init__(self, x, y, width, height, batch, window, *args, **kwargs):
        super(Menu, self).__init__(x, y, width, height, batch, *args, **kwargs)
        self.focus = None
        self.parent = None
        self.window = window
        self.branch = MenuBranch(x, y, width, height, batch, self, window)

    def _init_widget(self, widget, *args, **kwargs):
        assert isinstance(widget, MenuItem)
        super(Menu, self)._init_widget(widget, *args, **kwargs)
        self.set_focus(self.widgets.index(widget))

    def set_focus(self, i):
        """Set focus on widget at index `i`."""
        if i >= len(self.widgets):
            i = 0
        elif i < 0:
            i = len(self.widgets) - 1

        if self.focus is not None:
            self.widgets[self.focus].deselect()
        self.widgets[i].select()
        self.focus = i

    def trigger_focused(self):
        """Trigger the currently focused menu item."""
        focused = self.widgets[self.focus]
        if isinstance(focused, MenuBranch):
            self.window.pop_handlers()
            focused.menu.parent = self.branch
        focused.trigger()

    def descend(self):
        """Activate the previous menu."""
        if not self.parent:
            return
        self.window.pop_handlers()
        self.parent.trigger()

    def activate(self):
        """Activate the menu, pushing its event handlers on the window."""
        self.window.push_handlers(self)
    
    # event handlers ----------------------------------------------------------
    def on_draw(self):
        self.window.clear()
        self.batch.draw()
    
    def on_text_motion(self, motion):
        if motion is key.DOWN:
            self.set_focus(self.focus - 1)
        elif motion is key.UP:
            self.set_focus(self.focus + 1)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.trigger_focused()
        elif symbol == key.BACKSPACE:
            self.descend()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if not widget.selected and widget.hit_test(x, y):
                self.set_focus(self.widgets.index(widget))
                break

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == mouse.LEFT and
                self.widgets[self.focus].hit_test(x, y)):
            self.trigger_focused()
        elif button == mouse.RIGHT:
            self.descend()
