from unittest import TestCase

from mahjong import Player, Tile


class TestPlayer(TestCase):
    def test_add_to_hand(self):
        player = Player()
        player.add_to_hand(Tile.C1)
        hand = player.hand
        self.assertEqual(Tile.C1, hand[0])

    def test_discard(self):
        player = Player()
        player.add_to_hand(Tile.C1)
        player.discard(Tile.C1)
        self.assertEqual(0, len(player.hand))

    def test_add_to_decalaration(self):
        player = Player()
        player.add_to_decalaration(Tile.C1)
        self.assertEqual(Tile.C1, player.decalaration[0])
