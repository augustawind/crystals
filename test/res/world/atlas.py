ALL = ['RedRoom']
START = ('RedRoom', 1, 2, 2)


class RedRoom:

    key = {
        '|': 'vwall',
        '-': 'hwall',
        ',': 'rfloor',
        '+': 'sfloor'
    }

    map = [
        [
        ',,,,,',
        ',,,,,',
        ',,,,,',
        ',,,,,',
        ',,,,,',
        ],
        [
        '|---|',
        '|.+.|',
        '|+++|',
        '|.+.|',
        '|---|',
        ],
    ]
