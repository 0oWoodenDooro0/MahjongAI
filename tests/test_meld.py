from unittest import TestCase

from mahjong import TripletMeld, Tile, QuadrupletMeld, SequenceMeld


class TestTripletMeld(TestCase):
    def test_is_valid(self):
        self.assertTrue(TripletMeld.is_valid((Tile.C2, Tile.C2, Tile.C2)))
        self.assertFalse(TripletMeld.is_valid((Tile.C2, Tile.C2, Tile.C9)))


class TestSequenceMeld(TestCase):
    def test_is_valid(self):
        self.assertTrue(SequenceMeld.is_valid((Tile.C2, Tile.C3, Tile.C4)))
        self.assertFalse(SequenceMeld.is_valid((Tile.B8, Tile.B9, Tile.W1)))


class TestQuadrupletMeld(TestCase):
    def test_is_valid(self):
        self.assertTrue(QuadrupletMeld.is_valid((Tile.C2, Tile.C2, Tile.C2, Tile.C2)))
        self.assertFalse(QuadrupletMeld.is_valid((Tile.C2, Tile.C2, Tile.C9, Tile.C2)))
