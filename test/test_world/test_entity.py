import os
import sys

import pyglet

from crystals.world import entity, action
from test.util import *
from test.test_resource import imgloader


def TestEntity():
    image = imgloader().image('sack.png')
    batch = pyglet.graphics.Batch()
    entity_ = entity.Entity('an entity', True, image, batch,
                            facing=(0, 1), actions=[], x=2, y=2)

