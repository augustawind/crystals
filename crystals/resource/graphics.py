"""functions for loading and manipulating bundled images"""
import pyglet
from pyglet.gl import *

glEnable(GL_TEXTURE_2D)


def scale_image(img, width, height):
    """Scale `img` to `width` by `height`."""
    texture = img.get_texture()
    glBindTexture(GL_TEXTURE_2D, texture.id)
    texture.width = width
    texture.height = height
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

