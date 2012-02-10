ALL = ['Home']
START = ('Home', 1, 2, 2)


class Home:
    """The player character's home."""

    key = {
        '+': 'floor',
        '*': 'rug',
        '|': 'vwall',
        '-': 'hwall',
        'H': 'hwall_frame',
        'T': 'table',
        'b': 'chair_left',
        'd': 'chair_right',
        'B': 'bookcase',
        '^': 'dad'}
    
    map = [
        [
        '|-H---|',
        '|+++++|',
        '|+***+|',
        '|+***+|',
        '|+***+|',
        '|+++++|',
        '-------'
        ],
        [
        '.......',
        '....BB.',
        '.....^.',
        '.b.....',
        '...Td..',
        '.......',
        '.......'
        ]]

    portalkey = {}

    portalmap = []


class Slums:
    """The poor area of town."""


class Keep:
    """The nice area of town."""


class Hall:
    """The king's great hall."""
