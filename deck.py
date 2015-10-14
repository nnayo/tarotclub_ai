"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game

this file implements the interface with the server
and some basic classes
"""

from card import Card, Trump, Spade, Heart, Diamond, Club, str2cards

class Deck(object):
    """card deck"""

    def __init__(self, cards=None):
        self.cards = []

        if isinstance(cards, str):
            self.cards = str2cards(cards)
        elif isinstance(cards, list):
            for c in cards:
                self.cards.append(c)

        self.cards.sort()
        self.cards.reverse()

    def trumps(self):
        """extract the trumps"""
        return Deck([c for c in self.cards if isinstance(c, Trump)])

    def spades(self):
        """extract the spades"""
        return Deck([c for c in self.cards if isinstance(c, Spade)])

    def hearts(self):
        """extract the hearts"""
        return Deck([c for c in self.cards if isinstance(c, Heart)])

    def clubs(self):
        """extract the clubs"""
        return Deck([c for c in self.cards if isinstance(c, Club)])

    def diamonds(self):
        """extract the diamonds"""
        return Deck([c for c in self.cards if isinstance(c, Diamond)])

    def _evaluate_trumps(self):
        value = 0

        trumps = self.trumps()
        nb_trumps = len(trumps)

        if Trump(21) in trumps:
            value += 10

        if Trump(0) in trumps:
            value += 8

        if Trump(1) in trumps:
            if nb_trumps == 5:
                value += 5
            elif nb_trumps == 6:
                value += 7
            elif nb_trumps >= 7:
                value += 9

        if nb_trumps > 4:
            value += nb_trumps * 2

        major_trumps = [Trump(21), Trump(20), Trump(19), Trump(18), Trump(17), Trump(16)]
        for tr in major_trumps:
            if tr in trumps:
                value += 2

        suite = []
        prev_tr = trumps[0]
        for tr in trumps[1:]:
            if tr in major_trumps and prev_tr - tr == 1:
                if prev_tr not in suite:
                    suite.append(prev_tr)
                if tr not in suite:
                    suite.append(tr)
            prev_tr = tr
        value += len(suite)

        #print('trumps = %d' % value)
        return value

    def _evaluate_color(self, color):
        value = 0

        if Card(14) in color and Card(13) in color:
            value += 10
        elif Card(14) in color:
            value += 6
        elif Card(13) in color:
            value += 3

        if Card(12) in color:
            value += 2
        if Card(11) in color:
            value += 1

        if len(color) == 0:
            value += 6
        elif len(color) == 1:
            value += 3
        elif len(color) == 5:
            value += 5
        elif len(color) == 6:
            value += 7
        elif len(color) >= 7:
            value += 9
 
        #print('color = %d' % value)
        return value

    def evaluate(self):
        """
        return a note evaluating the strength of the deck
        see http://fftarot.fr/index.php/Decouvrir/Savoir-evaluer-son-jeu.html
        """
        value = 0

        value += self._evaluate_trumps()
        value += self._evaluate_color(self.spades())
        value += self._evaluate_color(self.hearts())
        value += self._evaluate_color(self.diamonds())
        value += self._evaluate_color(self.clubs())

        return value

    def __str__(self):
        """convert to a string"""
        return ';'.join(['%s' % c for c in self.cards])

    def _add_card(self, card):
        """add the given card to the deck"""
        self.cards.append(card)

    def __add__(self, other):
        """add card(s) into the deck"""
        # if adding 2 decks
        if isinstance(other, Deck):
            for card in other.cards:
                self._add_card(card)

        # else if add Card object
        elif isinstance(other, Card):
            self._add_card(other)

        self.cards.sort()
        self.cards.reverse()

        return self

    def _sub_card(self, card):
        """sub the given card from the deck"""
        self.cards.remove(card)

    def __sub__(self, other):
        """remove card(s) from the deck"""
        # if suppressing a deck
        if isinstance(other, Deck):
            for card in other.cards:
                self._sub_card(card)

        elif isinstance(other, Card):
            self._sub_card(other)

        return self

    def __len__(self):
        """return number of cards"""
        return len(self.cards)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.cards[i] != other.cards[i]:
                return False
        return True

    def __ne__(self, other):
        if len(self) != len(other):
            return True
        for i in range(len(self)):
            if self.cards[i] != other.cards[i]:
                return True
        return False

    def __iter__(self):
        for card in self.cards:
            yield card

    def __getitem__(self, key):
        return self.cards[key]

