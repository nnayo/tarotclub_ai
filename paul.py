"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game
"""

class Deck(object):
    """card deck"""

    _str2color_conv = {
        'T': 'trumps',
        'S': 'spades',
        'H': 'hearts',
        'C': 'clubs',
        'D': 'diamonds'
    }

    _color2str_conv = {
        'trumps': 'T',
        'spades': 'S',
        'hearts': 'H',
        'clubs': 'C',
        'diamonds': 'D',
    }

    def __init__(self):
        self.cards = {
            'trumps': [],
            'spades': [],
            'hearts': [],
            'clubs': [],
            'diamonds': []
        }

    def _add_card(self, card):
        """add the given card to the deck"""
        value = int(card[:2], 10)
        color = Deck._str2color_conv[card[3]]
        self.cards[color].append(value)

    @property
    def trumps(self):
        """extract the trumps"""
        return self.cards['trumps']

    @property
    def spades(self):
        """extract the spades"""
        return self.cards['spades']

    @property
    def hearts(self):
        """extract the hearts"""
        return self.cards['hearts']

    @property
    def clubs(self):
        """extract the clubs"""
        return self.cards['clubs']

    @property
    def diamonds(self):
        """extract the diamonds"""
        return self.cards['diamonds']

    def _from_string(self, string):
        """convert from string"""
        if len(string) == 0:
            return

        spl = string.split(';')
        for card in spl:
            self._add_card(card)

        for color in self.cards.values():
            color.sort()

    def __str__(self):
        """convert to a string"""
        deck = []
        for color in self.cards.keys():
            for card in self.cards[color]:
                string = '{value:02d}-{color}'
                deck.append(string.format(value=card, color=Deck._color2str_conv[color]))

        return ';'.join(deck)

    def __add__(self, other):
        """add card(s) into the deck"""
        # if adding 2 decks
        if type(other) == type(self):
            pass

        # else if add card(s) in string format
        elif type(other) == type(''):
            self._from_string(other)
            return self

class PaulAi(object):
    """the AI algo is done via the way of playing of my father named Paul"""
    def __init__(self):
        """set internal values"""

        self.place = None
        self.players = {
            'South': Deck(),
            'West': Deck(),
            'North': Deck(),
            'East': Deck(),
        }
        self.discard = Deck()
        self.taker = None
        self.contract = None
        self.handle = Deck()
        self.handle_team = None

        self.tricks = []

    def enter_game(self, place, mode):
        """
        place: South, West, North or East
        mode: one_deal or tournament (useless so far)
        """

        self.place = place

    def receive_cards(self, cards):
        """cards recevied as a string"""
        self.players[self.place] += cards

    def announce_bid(self):
        """announce the bid: Pass, Take, Guard, Guard without, Guard against"""
        # currently: pass
        self.contract = 'Pass'

        return self.contract

    def announce_slam(self):
        """announce a slam: True or False"""
        # currently: False
        if len(self.players[self.place].trumps) < 10:
            return False
        else:
            return True

    def build_discard(self, dog):
        """return the discard as a string"""
        self.players[self.place] += dog

        return '%s' % self.discard

    def start_deal(self, taker, contract):
        """
        game is about to start
        taker is the position of the taker: South, West, North, East
        contract is the contract played: Take, Guard, Guard without, Guard against
        """

        self.taker = taker
        self.contract = contract

    def ask_for_handle(self):
        """return the handle if any"""
        # TODO
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
        # TODO
        return ''

    def played_card(self, card, place):
        """give the card played by place"""

        self.players[place] += card

import unittest

class TestPaulAi(unittest.TestCase):
    """basic tests for AI"""

    def setUp(self):
        self.p_ai = PaulAi()
        self.dog = "04-C;13-C;10-C;12-D;21-T;07-T"
        self.players = {
            'South': "01-S;02-D;05-H;09-D;01-T;10-T;13-S;20-T;01-H;03-S;03-D;11-H;08-D;11-D;02-H;11-S;05-C;14-C",
            'West': "06-S;12-H;02-C;16-T;13-D;13-H;10-H;19-T;01-D;04-D;02-T;18-T;01-C;09-S;00-T;14-D;04-T;07-H",
            'North': "11-T;09-H;14-S;08-C;03-C;08-H;02-S;05-D;05-S;13-T;06-H;10-D;14-T;03-T;12-T;07-C;03-H;15-T",
            'East': "06-S;12-H;02-C;16-T;13-D;13-H;10-H;19-T;01-D;04-D;02-T;18-T;01-C;09-S;00-T;14-D;04-T;07-H",
        }

    def test_game_playing(self):
        """test a simple game playing session"""

        self.p_ai.enter_game('South', '')
        self.assertEqual(self.p_ai.place, 'South')

        print(dir(self.p_ai.players['South']))
        self.p_ai.receive_cards(self.players['South'])
        print(dir(self.p_ai.players['South']))
        self.assertEqual(self.p_ai.players['South'].cards, {
            'trumps': [1, 10, 20, ],
            'spades': [1, 3, 11, 13],
            'hearts': [1, 2, 5, 11],
            'clubs': [5, 14],
            'diamonds': [2, 3, 8, 9, 11],
        })

        bid = self.p_ai.announce_bid()
        self.assertEqual(bid, 'Pass')

        slam = self.p_ai.announce_slam()
        self.assertEqual(slam, False)

        dog = ''
        discard = self.p_ai.build_discard(dog)
        self.assertEqual(discard, '')

        self.p_ai.start_deal('North', 'Guard')
        self.assertEqual(self.p_ai.taker, 'North')
        self.assertEqual(self.p_ai.contract, 'Guard')

        handle = self.p_ai.ask_for_handle()
        self.assertEqual(handle, '')

        self.p_ai.show_handle('', '0')

        card = self.p_ai.play_card()
        self.assertEqual(card, '')

        petit = '01-T'
        self.p_ai.played_card(petit, 'North')
        self.assertEqual(self.p_ai.players['North'].cards['trumps'][0], 1)

if __name__ == '__main__':
    unittest.main()
