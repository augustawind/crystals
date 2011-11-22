import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label('Hello, world',
    font_name='Times New Roman',
    font_size=36,
    x=window.width//2, y=window.height//2,
    anchor_x='center', anchor_y='center')

image = pyglet.resource.image('data/img/char/dragon.png')

@window.event
def on_key_press(symbol, modifiers):
    print 'A key was pressed'

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
