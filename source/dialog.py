"""dialog.py"""

class Dialog:
    """Instantiation creates an iterator that produces a line at a time of
    formatted dialog text, e.g. 'John: Hello there!'
    """
    
    def __init__(self, char1, char2, text1, text2):        
        output = []
        for t1, t2 in zip(text1, text2):
            if t1:
                self.output.append('{}: {}'.format(char1.get_name(), t1))
            if t2:
                self.output.append('{}: {}'.format(char2.get_name(), t2))
        self.output = iter(output)

    def next(self):
        return self.output.next()