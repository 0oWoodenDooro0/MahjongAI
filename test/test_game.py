from unittest import TestCase

from game import Game


class TestGame(TestCase):
    def test_deal(self):
        game = Game()
        game.deal()
        for player in game.players:
            self.assertEqual(len(player.hand), 16)
        self.assertEqual(len(game.board.stack), 72)
