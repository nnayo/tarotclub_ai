"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game
"""

class Card(object):
    """generic card"""

    COLOR_STRENGTH = {'T': 4, 'S': 3, 'H': 2, 'D': 1, 'C': 0}
    COLOR = ['C', 'D', 'H', 'S', 'T', ' ']

    def __init__(self, value=0, color=''):
        self._value = value
        try:
            self._color = Card.COLOR_STRENGTH[color]
        except:
            self._color = 5 # generic color

    def __str__(self):
        string = '{value:02d}-{color}'
        return string.format(value=self._value, color=Card.COLOR[self._color])

    def __eq__(self, other):
        if self._color == 5 or other._color == 5:
            return self._value == other._value
        else:
            return self._color == other._color and self._value == other._value

    def __ne__(self, other):
        return self._color != other._color or self._value != other._value

    def __lt__(self, other):
        if self._color < other._color:
            return True

        if self._color == other._color and self._value < other._value:
            return True

        return False

    def __le__(self, other):
        if self._color < other._color:
            return True

        if self._value <= other._value:
            return True

        return False

    def __sub__(self, other):
        return (self._color - other._color) * 100 + (self._value - other._value)

class Trump(Card):
    def __init__(self, value):
        super().__init__(value, 'T')

class Spade(Card):
    def __init__(self, value):
        super().__init__(value, 'S')

class Heart(Card):
    def __init__(self, value):
        super().__init__(value, 'H')

class Club(Card):
    def __init__(self, value):
        super().__init__(value, 'C')

class Diamond(Card):
    def __init__(self, value):
        super().__init__(value, 'D')


def str2cards(strng):
    """convert a card(s) representating string to a list of Card objects"""

    def str2card(strng):
        """convert a single card representating string to a Card object"""
        value = int(strng[:2], 10)

        if '-T' in strng:
            return Trump(value)
        elif '-S' in strng:
            return Spade(value)
        elif '-H' in strng:
            return Heart(value)
        elif '-C' in strng:
            return Club(value)
        elif '-D' in strng:
            return Diamond(value)

    res = []
    for splt in strng.split(';'):
        res.append(str2card(splt))
    
    return res

