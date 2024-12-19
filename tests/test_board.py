from unittest import TestCase

from mahjong import Board, Tile


class TestBoard(TestCase):
    def test_deal(self):
        board = Board()
        board.draw()
        self.assertEqual(len(board.wall), 135)

    def test_discard_to_river(self):
        board = Board()
        board.discard_to_river(Tile.B1)
        self.assertEqual(len(board.river), 1)
        self.assertEqual(board.river[0], Tile.B1)
