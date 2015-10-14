"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game
"""

from card import Card, Trump, Spade, Heart, Diamond, Club
from deck import Deck

class Ai(object):
    """this AI algo is very stupid, it only follows the rules"""
    def __init__(self, interf):
        self.interf = interf

    def announce_bid(self):
        """announce the bid: Pass, Take, Guard, Guard without, Guard against"""
        value = self.interf.deck.evaluate()
        if value < 40:
            contract = 'Pass'
        elif value < 55:
            contract = 'Take'
        elif value < 70:
            contract = 'Guard'
        elif value < 80:
            contract = 'Guard without'
        else:
            contract = 'Guard against'

        return contract

    def announce_slam(self):
        """announce a slam: True or False"""
        # currently: False
        return False

    def build_discard(self):
        """return the discard"""
        # stupid algo: choose 6 cards from colors except kings
        cards = [c for c in self.interf.deck if not isinstance(c, Trump) and not c is Card(14)]
        cards = cards[:6]

        discard = Deck()

        for card in cards:
            discard += card

        return discard

    def ask_for_handle(self):
        """return the handle if any"""
        handle = self.interf.deck.trumps()

        if len(handle) >= 10:
            # don't show unnecessary higher trumps but the highest
            while len(handle) > 10:
                del handle[1]

            return handle
        else:
            return Deck()

    def play_card(self):
        """return the card to play"""
        # first to play on this trick?
        if self.interf.trick_place == 1:
            # stupid algo: play the first card from the deck...
            card = self.interf.deck[0]

        else:
            # retreive the first card played on this trick
            first_card = self.interf.trick[0]

            # check if we have this color
            if isinstance(first_card, Trump):
                wanted = self.interf.deck.trumps()
            elif isinstance(first_card, Spade):
                wanted = self.interf.deck.spades()
            elif isinstance(first_card, Heart):
                wanted = self.interf.deck.heart()
            elif isinstance(first_card, Diamond):
                wanted = self.interf.deck.diamond()
            elif isinstance(first_card, Club):
                wanted = self.interf.deck.clubs()

            if len(wanted) != 0:
                card = wanted[0]

        return card
