from unittest import TestCase
from mahjong import Tile


class TestTile(TestCase):
    def test_get_tile_seq(self):
        self.assertEqual(Tile.B1.get_tile_seq(), 1)
        self.assertEqual(Tile.W1.get_tile_seq(), 0)

    def test_next_seq_tile(self):
        self.assertEqual(Tile.B1.next_seq_tile(), Tile.B2)
        self.assertEqual(Tile.B7.next_seq_tile(2), Tile.B9)
        self.assertEqual(Tile.B9.next_seq_tile(), -1)
        self.assertEqual(Tile.W1.next_seq_tile(), -1)
        self.assertRaises(ValueError, Tile.W1.next_seq_tile, -1)
