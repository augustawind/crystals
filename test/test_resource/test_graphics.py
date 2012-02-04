import pyglet

from crystals.resource import graphics
from test.util import *
from test.test_resource import imgloader

images = imgloader()


def TestScaleImage_ValidParamsGiven_ScaleImage():
    img = images.image('cow.png')
    texture = img.get_texture()
    assert texture.width != 13
    assert texture.height != 13

    graphics.scale_image(img, 13, 13)
    assert texture.width == 13
    assert texture.height == 13
