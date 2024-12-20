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
        self.assertRaises(ValueError, player.discard, Tile.C2)

    def test_add_to_declaration(self):
        player = Player(0)
        player.add_to_declaration((Tile.C1, Tile.C2, Tile.C3))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0])

    def test_add_kong(self):
        player = Player(0)
        player.add_to_declaration((Tile.C1, Tile.C2, Tile.C3))
        player.add_to_declaration((Tile.D3, Tile.D3, Tile.D3))
        player.add_to_declaration((Tile.D7, Tile.D8, Tile.D9))
        player.add_kong(Tile.D3)
        self.assertEqual(player.declaration[1], (Tile.D3, Tile.D3, Tile.D3, Tile.D3))
