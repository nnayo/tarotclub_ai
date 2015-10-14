"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game

this file implements the interface with the server
and some basic classes
"""

from card import str2cards
from deck import Deck

# import the available AI
import baby
import paul

class AiInterface(object):
    """the AI algo is done via the way of playing of my father named Paul"""
    def __init__(self, ai=baby.Ai):
        """set internal values"""

        self.place = None
        self.decks = {
            'South': Deck(),
            'East': Deck(),
            'North': Deck(),
            'West': Deck(),
        }
        self.discard = Deck()
        self.taker = None
        self.contract = None
        self.handle = { 'deck': Deck(), 'team': None}

        self.trick_rank = 0
        self.trick_place = 0
        self.trick = []

        self.ai = ai(self)

    def deck_get(self):
        """return own deck"""
        if self.place:
            return self.decks[self.place]
        else:
            return Deck()

    def deck_set(self, deck):
        self.decks[self.place] = deck

    deck = property(deck_get, deck_set)

    def enter_game(self, place, mode):
        """
        place: South, East, North or West
        mode: one_deal or tournament (useless so far)
        """
        self.place = place

    def receive_cards(self, cards):
        """cards recevied as a string"""
        self.deck = Deck(cards)

    def announce_bid(self):
        """announce the bid: Pass, Take, Guard, Guard without, Guard against"""
        self.contract = self.ai.announce_bid()

        return self.contract

    def announce_slam(self):
        """announce a slam: True or False"""
        return self.ai.announce_slam()

    def build_discard(self, dog):
        """return the discard as a string"""
        self.deck += Deck(dog)

        self.discard = self.ai.build_discard()

        return '%s' % self.discard

    def start_deal(self, taker, contract):
        """
        game is about to start
        taker is the position of the taker: South, East, North, West
        contract is the contract played: Take, Guard, Guard without, Guard against
        """

        self.taker = taker
        self.contract = contract

    def ask_for_handle(self):
        """return the handle if any"""
        self.handle = self.ai.ask_for_handle()

        return '%s' % self.handle

    def show_handle(self, handle, team):
        """
        handle: cards in string
        team: '0' if declared by attack, '1' if defense
        """
        self.handle += handle
        self.handle_team = {'0': 'attack', '1': 'defense'}[team]

    def play_card(self):
        """return the card to play"""
        self.trick_place += 1
        self.trick_place %= 4

        print('trick_place = %d' % self.trick_place)

        card = self.ai.play_card()

        self.deck -= card
        self.trick.append(card)

        return '%s' % card

    def played_card(self, card, place):
        """give the card played by place"""
        self.trick_place += 1
        self.trick_place %= 4

        if self.trick_place == 1:
            self.trick = []

        print('played_card = %s' % card)
        self.decks[place] += card
        self.trick.append(str2cards(card)[0])

