"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game
"""

class Card(object):
    """generic card"""
    def __init__(self, value=0, color=''):
        self._value = value
        self._color = color

    def __str__(self):
        string = '{value:02d}-{color}'
        return string.format(value=self._value, color=self._color)

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


def str2card(strng):
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
        for color in ('trumps', 'spades', 'hearts', 'clubs', 'diamonds'):
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

    def __len__(self):
        """return number of cards"""
        return len(self.trumps) + len(self.spades) + len(self.hearts) \
                + len(self.clubs) + len(self.diamonds)

class PaulAi(object):
    """the AI algo is done via the way of playing of my father named Paul"""
    def __init__(self):
        """set internal values"""

        self.place = None
        self.decks = {
            'self': Deck(),
            'South': Deck(),
            'East': Deck(),
            'North': Deck(),
            'West': Deck(),
        }
        self.discard = Deck()
        self.taker = None
        self.contract = None
        self.handle = { 'deck': Deck(), 'team': None}

        self.tricks = []

    @property
    def deck(self):
        """return own deck"""
        return self.decks['self']

    def enter_game(self, place, mode):
        """
        place: South, East, North or West
        mode: one_deal or tournament (useless so far)
        """
        self.place = place
        self.decks['self'] = self.decks[place]

    def receive_cards(self, cards):
        """cards recevied as a string"""
        self.decks['self'] += cards

    def announce_bid(self):
        """announce the bid: Pass, Take, Guard, Guard without, Guard against"""
        # currently algo: if 'excuse' => Take
        if 0 in self.deck.trumps:
            self.contract = 'Take'
        else:
            self.contract = 'Pass'

        return self.contract

    def announce_slam(self):
        """announce a slam: True or False"""
        # currently: False
        if len(self.decks[self.place].trumps) < 10:
            return False
        else:
            return True

    def build_discard(self, dog):
        """return the discard as a string"""
        self.decks[self.place] += dog

        # stupid algo: choose 6 cards from colors except kings
        while len(self.discard) < 6:
            if len(self.deck.spades) != 0 and self.deck.spades[0] != 14:
                self.discard += '%02d-S' % self.deck.spades[0]
                del self.deck.spades[0]
                continue

            if len(self.deck.hearts) != 0 and self.deck.hearts[0] != 14:
                self.discard += '%02d-H' % self.deck.hearts[0]
                del self.deck.hearts[0]
                continue

            if len(self.deck.clubs) != 0 and self.deck.clubs[0] != 14:
                self.discard += '%02d-C' % self.deck.clubs[0]
                del self.deck.clubs[0]
                continue

            if len(self.deck.diamonds) != 0 and self.deck.diamonds[0] != 14:
                self.discard += '%02d-D' % self.deck.diamonds[0]
                del self.deck.diamonds[0]
                continue

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
        if len(self.deck.trumps) >= 10:
            self.handle = self.deck.trumps
            # don't show unnecessary higher trumps but the highest
            delta = 10 - len(self.handle)
            if delta > 0:
                self.handle = self.handle[-delta - 1 : -delta]
        else:
            self.handle = ''

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
        # stupid algo
        if len(self.deck.trumps) != 0:
            card = self.deck.trumps[0]
            del self.deck.trumps[0]
            return '%02d-T' % card

        if len(self.deck.spades) != 0:
            card = self.deck.spades[0]
            del self.deck.spades[0]
            return '%02d-S' % card

        if len(self.deck.hearts) != 0:
            card = self.deck.hearts[0]
            del self.deck.hearts[0]
            return '%02d-H' % card

        if len(self.deck.clubs) != 0:
            card = self.deck.clubs[0]
            del self.deck.clubs[0]
            return '%02d-C' % card

        if len(self.deck.diamonds) != 0:
            card = self.deck.diamonds[0]
            del self.deck.diamonds[0]
            return '%02d-D' % card

        return ''

    def played_card(self, card, place):
        """give the card played by place"""

        self.decks[place] += card

import unittest

class TestPaulAi(unittest.TestCase):
    """basic tests for AI"""

    def setUp(self):
        self.p_ai = { 'South': PaulAi(), 'East': PaulAi(), 'North': PaulAi(), 'West': PaulAi(), }
        self.deals = {
            'dog': "04-C;13-C;10-C;12-D;21-T;07-T",
            'South': "01-S;02-D;05-H;09-D;01-T;10-T;13-S;20-T;01-H;03-S;03-D;11-H;08-D;11-D;02-H;11-S;05-C;14-C",
            'East': "06-S;12-H;02-C;16-T;13-D;13-H;10-H;19-T;01-D;04-D;02-T;18-T;01-C;09-S;00-T;14-D;04-T;07-H",
            'North': "11-T;09-H;14-S;08-C;03-C;08-H;02-S;05-D;05-S;13-T;06-H;10-D;14-T;03-T;12-T;07-C;03-H;15-T",
            'West': "05-T;06-T;08-T;09-T;17-T;04-S;07-S;08-S;10-S;12-S;04-H;14-H;06-C;09-C;11-C;12-C;06-D;07-D",
        }

    def test_game_playing(self):
        """test a simple game playing session"""

        player_decks = {
            'South': {
                'trumps': [1, 10, 20, ],
                'spades': [1, 3, 11, 13, ],
                'hearts': [1, 2, 5, 11, ],
                'clubs': [5, 14, ],
                'diamonds': [2, 3, 8, 9, 11, ],
            },
            'East': {
                'trumps': [0, 2, 4, 16, 18, 19, ],
                'spades': [6, 9, ],
                'hearts': [7, 10, 12, 13, ],
                'clubs': [1, 2, ],
                'diamonds': [1, 4, 13, 14, ],
            },
            'North': {
                'trumps': [3, 11, 12, 13, 14, 15, ],
                'spades': [2, 5, 14, ],
                'hearts': [3, 6, 8, 9, ],
                'clubs': [3, 7, 8, ],
                'diamonds': [5, 10, ],
            },
            'West': {
                'trumps': [5, 6, 8, 9, 17, ],
                'spades': [4, 7, 8, 10, 12, ],
                'hearts': [4, 14, ],
                'clubs': [6, 9, 11, 12, ],
                'diamonds': [6, 7, ],
            },
        }

        player_bids = {
            'South': 'Pass',
            'East': 'Take',
            'North': 'Pass',
            'West': 'Pass',
        }

        for player in ('South', 'East', 'North', 'West'):
            self.p_ai[player].enter_game(player, '')
            self.assertEqual(self.p_ai[player].place, player)

            self.p_ai[player].receive_cards(self.deals[player])
            self.assertEqual(self.p_ai[player].deck.cards, player_decks[player])

        taker = 'South'
        bid = 'Pass'
        for player in ('South', 'East', 'North', 'West'):
            _bid = self.p_ai[player].announce_bid()
            self.assertEqual(_bid, player_bids[player])
            if _bid != 'Pass':
                taker = player
                bid = _bid

        for player in ('South', 'East', 'North', 'West'):
            slam = self.p_ai[player].announce_slam()
            self.assertEqual(slam, False)

        discard = self.p_ai[taker].build_discard(self.deals['dog'])
        self.assertEqual(discard, '06-S;09-S;07-H;10-H;12-H;13-H')

        for player in ('South', 'East', 'North', 'West'):
            self.p_ai[player].start_deal(taker, bid)
            self.assertEqual(self.p_ai[player].taker, taker)
            self.assertEqual(self.p_ai[player].contract, bid)

        handle = ''
        for player in ('South', 'East', 'North', 'West'):
            _handle = self.p_ai[player].ask_for_handle()
            self.assertEqual(_handle, '')
            if _handle is not '':
                handle = _handle

        for player in ('South', 'East', 'North', 'West'):
            self.p_ai[player].show_handle(handle, '0')

        for trick in range(18):
            players = ('South', 'East', 'North', 'West')
            for player in players:
                card = self.p_ai[player].play_card()
                print('player/card : %s -> %s' % (player, card))

                sub_players = list(players)
                sub_players.remove(player)
                for sub_player in sub_players:
                    self.p_ai[player].played_card(card, player)

if __name__ == '__main__':
    unittest.main()
