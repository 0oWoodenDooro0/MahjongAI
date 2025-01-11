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
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C2)
        player.add_to_hand(Tile.C3)
        player.add_to_declaration((Tile.C1, Tile.C2, Tile.C3))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0])

    def test_chow(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C3)
        player.chow((Tile.C1, Tile.C2, Tile.C3), Tile.C2)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0])

    def test_pong(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.pong((Tile.C1, Tile.C1, Tile.C1), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1), player.declaration[0])

    def test_kong(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.kong((Tile.C1, Tile.C1, Tile.C1, Tile.C1), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0])

    def test_closed_kong(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.closed_kong((Tile.C1, Tile.C1, Tile.C1, Tile.C1))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0])

    def test_add_kong(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C1)
        player.pong((Tile.C1, Tile.C1, Tile.C1), Tile.C1)
        player.add_to_hand(Tile.C1)
        player.add_kong(Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0])

    def test_get_mask(self):
        player = Player(0)
        player.add_to_hand(Tile.C1)
        player.add_to_hand(Tile.C2)
        mask = player.get_mask()
        for i in range(34):
            if i == 0 or i == 1:
                self.assertEqual(1, mask[i])
            else:
                self.assertEqual(0, mask[i])

    def test_str(self):
        player = Player(0)
        self.assertEqual(str(player), "Player 0")

