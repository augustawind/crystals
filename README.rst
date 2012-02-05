CRYSTALS
========
A top-down RPG/Adventure based on the album CRYSTALS by `Julian Wass <http://julianwass.bandcamp.com>`_
-------------------------------------------------------------------------------------------------------

Crystals is currently under active development by me, Dustin Rohde, and
is considered to be in alpha. Active development is currently taking
place in the 'xp' branch.

You must have `python <http://python.org>` 2.7.2 and `pyglet <http://pyglet.org>`_ >= 1.1.4
installed to run crystals properly. It is not yet known whether crystals runs
properly on any operating system other than Linux, and with any previous
versions of pyglet.

To run the game, use python to execute 'run.py'::
    
    cd crystals
    python run.py

To run the test suite, you must have nose >= 1.1.2 installed. To run the
entire test suite, issue the following commands::

    cd crystals
    nosetests test

Nose is configured in 'setup.cfg'.
