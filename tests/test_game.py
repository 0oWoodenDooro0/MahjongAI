from unittest import TestCase

from mahjong import Game, Tile


class TestGame(TestCase):
    def test_deal(self):
        game = Game()
        game.deal()
        for player in game.players:
            self.assertEqual(16, len(player.hand))
        self.assertEqual(72, len(game.board.wall))

    def test_draw(self):
        game = Game()
        game.draw()
        self.assertEqual(len(game.board.wall), 135)
        game.board.wall = [Tile.C2, Tile.C2, Tile.C2]
        self.assertIsNone(game.draw())
        self.assertTrue(game.over)

    def test_get_discard_tile(self):
        game = Game()
        game.board.discard_to_river(Tile.C2)
        self.assertEqual(Tile.C2, game.get_discard_tile())

    def test_get_turn_player(self):
        game = Game()
        game.turn = 1
        self.assertEqual(game.players[1], game.get_turn_player())

    def test_turn_next(self):
        game = Game()
        game.turn = 3
        game.turn_next()
        self.assertEqual(0, game.turn)
