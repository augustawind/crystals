import pyglet

from crystals.resource import graphics
from test.util import *


def TestScaleImage_ValidParamsGiven_ScaleImage():
    img = load_image('cow.png')
    texture = img.get_texture()
    assert texture.width != 13
    assert texture.height != 13

    graphics.scale_image(img, 13, 13)
    assert texture.width == 13
    assert texture.height == 13
