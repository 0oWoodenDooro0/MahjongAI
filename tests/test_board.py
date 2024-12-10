from unittest import TestCase

from mahjong import Board, Player


class TestBoard(TestCase):
    def test_deal(self):
        board = Board()
        player = Player()
        board.deal(player)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(len(board.wall), 135)
