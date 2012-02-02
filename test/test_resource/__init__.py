import os
import sys

import pyglet
from nose.tools import *

from crystals import resource
from crystals import entity
from test.util import *


@raises(resource.ResourceError)
def TestResourceError():
    raise resource.ResourceError()
