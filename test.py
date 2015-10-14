#! /usr/bin/env python3

"""
tarotclub game python AI

this is a try to make a python AI for the tarotclub game

this file implements the interface with the server
and some basic classes
"""

from card import Trump, Spade, Heart, Diamond, Club, str2cards
from deck import Deck
import interface

# import the available AI
import baby
import paul

import unittest

class TestAiInterface(unittest.TestCase):
    """basic tests for AI"""

    def setUp(self):
        self.p_ai = {
            'South': interface.AiInterface(baby.Ai),
            'East': interface.AiInterface(baby.Ai),
            'North': interface.AiInterface(paul.Ai),
            'West': interface.AiInterface(paul.Ai),
        }
        self.deal = {
            'dog': "04-C;13-C;10-C;12-D;21-T;07-T",
            'South': "01-S;02-D;05-H;09-D;01-T;10-T;13-S;20-T;01-H;03-S;03-D;11-H;08-D;11-D;02-H;11-S;05-C;14-C",
            'East': "06-S;12-H;02-C;16-T;13-D;13-H;10-H;19-T;01-D;04-D;02-T;18-T;01-C;09-S;00-T;14-D;04-T;07-H",
            'North': "11-T;09-H;14-S;08-C;03-C;08-H;02-S;05-D;05-S;13-T;06-H;10-D;14-T;03-T;12-T;07-C;03-H;15-T",
            'West': "05-T;06-T;08-T;09-T;17-T;04-S;07-S;08-S;10-S;12-S;04-H;14-H;06-C;09-C;11-C;12-C;06-D;07-D",
        }

    def test_card(self):
        """test Card object"""
        self.assertTrue(Trump(2) == Trump(2))
        self.assertTrue(Trump(2) != Trump(1))
        self.assertTrue(Trump(2) > Trump(1))
        self.assertTrue(Trump(2) >= Trump(1))
        self.assertTrue(Trump(2) > Spade(10))
        self.assertTrue(Trump(2) >= Spade(10))
        self.assertTrue(Spade(10) < Trump(1))
        self.assertTrue(Spade(10) <= Trump(1))
        self.assertTrue(Diamond(9) > Club(14))
        self.assertTrue(Club(14) < Diamond(9))
        self.assertTrue(Trump(1) > Diamond(2))

    def test_card_helpers(self):
        """test helper functions"""
        self.assertEqual(str2cards('06-C'), [Club(6), ])

        self.assertEqual(str2cards('01-T;02-S;03-H;04-D'), [Trump(1), Spade(2), Heart(3), Diamond(4)])

    def test_deck(self):
        """test deck functions"""
        deck = Deck()

        deck += Trump(2)
        self.assertEqual(len(deck), 1)
        self.assertEqual(deck.trumps(), Deck([Trump(2), ]))

        deck2 = Deck()
        deck2 += Trump(1)
        deck2 += Trump(3)
        deck2 += Heart(13)
        deck2 += Club(13)
        deck2 += Diamond(13)
        deck += deck2
        self.assertEqual(len(deck), 6)
        self.assertEqual(deck.trumps(), Deck([Trump(3), Trump(2), Trump(1)]))
        self.assertEqual('%s' % deck, '03-T;02-T;01-T;13-H;13-D;13-C')

        deck -= Trump(2)
        self.assertEqual(len(deck), 5)
        self.assertEqual(deck.trumps(), Deck([Trump(3), Trump(1)]))

        deck -= deck2
        self.assertEqual(len(deck), 0)

        deck = Deck('21-T;19-T;12-T;06-T;01-T;00-T;14-S;12-S;10-S;08-S;01-S;11-H;08-H;13-D;12-D;07-D;06-C;04-C')
        # evaluation :
        #   trumps   41 = 10 + 8 + 7 + 12 + 4
        #   spades   13 = 6 + 2 + 5
        #   hearts    1 = 1
        #   diamonds  5 = 3 + 2
        #   clubs     0 = 0
        #      sum = 60

        self.assertEqual(deck.evaluate(), 60)

        deck = Deck('20-T;18-T;14-T;13-T;09-T;08-T;06-T;14-S;10-S;05-S;04-S;14-H;13-H;08-D;07-D;08-C;07-C;05-C')
        # evaluation :
        #   trumps   18 = 14 + 4
        #   spades    6 = 6
        #   hearts   10 = 10
        #   diamonds  0 = 0
        #   clubs     0 = 0
        #      sum = 34

        self.assertEqual(deck.evaluate(), 34)

        deck = Deck('21-T;20-T;19-T;16-T;14-T;12-T;08-T;00-T;14-S;13-S;08-S;05-S;02-S;04-H;14-D;09-C;08-C;03-C')
        # evaluation :
        #   trumps   45 = 10 + 8 + 16 + 8 + 3
        #   spades   15 = 10 + 5
        #   hearts    3 = 3
        #   diamonds  9 = 6 + 3
        #   clubs     0 = 0
        #      sum = 72

        self.assertEqual(deck.evaluate(), 72)

        deck = Deck('21-T;18-T;17-T;11-T;07-T;01-T;00-T;14-S;13-S;12-S;11-S;10-S;08-S;05-S;14-H;13-D;05-D;04-D')
        # evaluation :
        #   trumps   49 = 10 + 8 + 9 + 14 + 6 + 2
        #   spades   22 = 10 + 2 + 1 + 9
        #   hearts    9 = 6 + 3
        #   diamonds  3 = 3
        #   clubs     6 = 6
        #      sum = 89

        self.assertEqual(deck.evaluate(), 89)

    def test_game_playing(self):
        """test a simple game playing session"""

        player_decks = {
            'South':
                Deck('01-T;10-T;20-T;01-S;03-S;11-S;13-S;01-H;02-H;05-H;11-H;05-C;14-C;02-D;03-D;08-D;09-D;11-D'),
            'East':
                Deck('00-T;02-T;04-T;16-T;18-T;19-T;06-S;09-S;07-H;10-H;12-H;13-H;01-C;02-C;01-D;04-D;13-D;14-D'),
            'North':
                Deck('03-T;11-T;12-T;13-T;14-T;15-T;02-S;05-S;14-S;03-H;06-H;08-H;09-H;03-C;07-C;08-C;05-D;10-D'),
            'West':
                Deck('05-T;06-T;08-T;09-T;17-T;04-S;07-S;08-S;10-S;12-S;04-H;14-H;06-C;09-C;11-C;12-C;06-D;07-D'),
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

            self.p_ai[player].receive_cards(self.deal[player])
            self.assertEqual(self.p_ai[player].deck, player_decks[player])

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

        discard = self.p_ai[taker].build_discard(self.deal['dog'])
        self.assertEqual(discard, '09-S;06-S;13-H;12-H;10-H;07-H')

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

        #for trick in range(18):
        for trick in range(2):
            players = ('South', 'East', 'North', 'West')
            for player in players:
                card = self.p_ai[player].play_card()
                print('player/card : %s -> %s' % (player, card))

                sub_players = list(players)
                sub_players.remove(player)
                for sub_player in sub_players:
                    self.p_ai[sub_player].played_card(card, player)

if __name__ == '__main__':
    unittest.main()
