from unittest import TestCase

from mahjong import Player, Tile


class TestPlayer(TestCase):
    def test_add_to_hand(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        hand = player.hand
        self.assertEqual(Tile.C1, hand[0])

    def test_discard(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.discard(Tile.C1)
        self.assertEqual(0, len(player.hand))

    def test_add_to_declaration(self):
        player = Player(0)
        player.add_to_declaration((Tile.C1, Tile.C2, Tile.C3))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0])
