#!/usr/bin/python2
"""runs the game"""
import sys
import os.path
import subprocess

from crystals.game import Game

TEST_PKGS = ['crystals/test']

if __name__ == '__main__':
    if os.path.split(sys.argv[0])[-1] == 'run.py' and len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            # Run the test suite with the given args
            subprocess.call(['nosetests2'] + sys.argv[2:] + TEST_PKGS)
        else:
            # Call python2 with all args given to ./run.py
            subprocess.call(['python2'] + sys.argv[1:] + ['run.py'])
    else:
        game = Game()
        game.run()
