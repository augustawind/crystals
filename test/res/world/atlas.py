ALL = ['RedRoom']
START = 'RedRoom'


class RedRoom:

    key = {
        '|': 'vwall',
        '-': 'hwall',
        ',': 'floor_rough',
        '+': 'floor_smooth'
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
