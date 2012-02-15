from crystals.scripthelpers import *


troll_action = ActionIter(
    Talk('I like shorts.'),
    ActionSequence(
        UpdatePlot('CheckTroll'),
        Talk("Don't you, punk?!")),
    Talk('I like shorts.'))
