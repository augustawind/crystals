ROOMS = ['RedRoom', 'BlueRoom']
START = ('RedRoom', 1, 2, 2)


class RedRoom:

    key = {
        '|': 'vwall',
        '-': 'hwall',
        ',': 'rfloor',
        '+': 'sfloor',
        'T': 'troll',}
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
        '|.T.|',
        '-----',
        ],]

    portalkey = {
        'B': 'BlueRoom',}
    portalmap = [
        ".....",
        ".....",
        "...B.",
        ".....",
        ".....",]

class BlueRoom:

    key = {
        '|': 'vwall',
        '-': 'hwall',
        ',': 'rfloor',
        '+': 'sfloor',}
    map = [
        [
        '|-+-|',
        '-+-+-',
        '+++++',
        '|+-+|',
        '--+--',
        ]]

    portalkey = {
        'R': 'RedRoom',}
    portalmap = [
        ".....",
        ".....",
        "..R..",
        ".....",
        ".....",]
