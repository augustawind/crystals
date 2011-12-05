#!/usr/bin/python

"""run.py"""

import logging
import sys

from crystals.game import Game

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout,
        format='%(levelname)s:%(message)s')

    game = Game()
    game.run()
