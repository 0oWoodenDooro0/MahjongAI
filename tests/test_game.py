from unittest import TestCase

from mahjong import Game, Tile


class TestGame(TestCase):
    def test_deal(self):
        game = Game()
        for player in game.players:
            self.assertEqual(len(player.hand), 16)
        self.assertEqual(len(game.board.wall), 72)

    def test_draw(self):
        game = Game()
        game.draw()
        self.assertEqual(len(game.board.wall), 71)
        game.board.wall = [Tile.C2, Tile.C2, Tile.C2]
        self.assertIsNone(game.draw())
        self.assertTrue(game.over)

    def test_get_discard_tile(self):
        game = Game()
        game.board.discard_to_river(Tile.C2)
        self.assertEqual(game.get_discard_tile(), Tile.C2)

    def test_get_turn_player(self):
        game = Game()
        game.turn = 1
        self.assertEqual(game.get_turn_player(), game.players[1])

    def test_turn_next(self):
        game = Game()
        game.turn = 3
        game.turn_next()
        self.assertEqual(game.turn, 0)
