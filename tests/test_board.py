from unittest import TestCase

import numpy as np

from mahjong import Board, Tile


class TestBoard(TestCase):
    def test_draw(self):
        board = Board()
        board.draw()
        self.assertEqual(len(board.wall), 135)
        board.wall = [Tile.D3]
        self.assertIsNone(board.draw())

    def test_discard_to_river(self):
        board = Board()
        board.discard_to_river(Tile.B1)
        self.assertEqual(len(board.river), 1)
        self.assertEqual(board.river[0], Tile.B1)

    def test_get_last_discard_tile(self):
        board = Board()
        board.discard_to_river(Tile.B1)
        self.assertEqual(board.get_last_discard_tile(), Tile.B1)
        self.assertEqual(len(board.river), 0)

    def test_river_observation(self):
        board = Board()
        board.discard_to_river(Tile.C1)
        np.testing.assert_equal(np.asarray([np.asarray(
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                            np.zeros(34), np.zeros(34), np.zeros(34)]), board.river_observation())
