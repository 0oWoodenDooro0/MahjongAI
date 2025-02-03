from unittest import TestCase

from mahjong import Player, Tile, SequenceMeld, TripletMeld, QuadrupletMeld


class TestPlayer(TestCase):
    def test_add_to_hand(self):
        player = Player(0)
        player.draw(Tile.C1)
        hand = player.hand
        self.assertEqual(Tile.C1, hand[0])

    def test_discard(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.discard(Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertRaises(ValueError, player.discard, Tile.C2)

    def test_add_to_declaration(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C2)
        player.draw(Tile.C3)
        player.add_to_declaration(SequenceMeld((Tile.C1, Tile.C2, Tile.C3)))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0].tiles)

    def test_chow(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C3)
        player.chow(SequenceMeld((Tile.C1, Tile.C2, Tile.C3)), Tile.C2)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C2, Tile.C3), player.declaration[0].tiles)

    def test_pong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.pong(TripletMeld((Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.kong(QuadrupletMeld((Tile.C1, Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_closed_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.closed_kong(QuadrupletMeld((Tile.C1, Tile.C1, Tile.C1, Tile.C1)))
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)

    def test_add_kong(self):
        player = Player(0)
        player.draw(Tile.C1)
        player.draw(Tile.C1)
        player.pong(TripletMeld((Tile.C1, Tile.C1, Tile.C1)), Tile.C1)
        player.draw(Tile.C1)
        player.add_kong(Tile.C1)
        self.assertEqual(0, len(player.hand))
        self.assertEqual((Tile.C1, Tile.C1, Tile.C1, Tile.C1), player.declaration[0].tiles)
