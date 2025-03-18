from unittest import TestCase

from mahjong import (
    Game,
    Tile,
    TripletMeld,
    Declaration,
    Action,
    SequenceMeld,
    QuadrupletMeld,
)


class TestGame(TestCase):
    def test_init_game(self):
        game = Game()
        game.init_game()
        self.assertEqual(17, len(game.players[0].hand))
        self.assertEqual(16, len(game.players[1].hand))
        self.assertEqual(16, len(game.players[2].hand))
        self.assertEqual(16, len(game.players[3].hand))
        self.assertEqual(71, len(game.board.wall))
        self.assertEqual(0, game.turn)
        self.assertFalse(game.over)
        self.assertEqual(1, len(game.next_step))

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

    def test_win(self):
        game = Game()
        game.win()
        self.assertTrue(game.over)

    def test_check_discard_next_step(self):
        game = Game()
        game.players[0].hand.tiles = [Tile.C2, Tile.C2, Tile.C2]
        game.players[3].hand.tiles = [Tile.D3, Tile.D3, Tile.C7, Tile.C7]
        game.players[2].hand.tiles = [Tile.C7, Tile.C7, Tile.C7]
        game.players[1].hand.tiles = [Tile.C6, Tile.C8, Tile.C8]
        next_step = game.check_discard_next_step(Tile.C7)
        self.assertEqual(5, len(next_step))

    def test_check_draw_next_step(self):
        game = Game()
        game.players[0].hand.tiles = [Tile.D3, Tile.C6, Tile.C8]
        game.players[0].declaration = Declaration(
            [
                TripletMeld((Tile.D3, Tile.D3, Tile.D3)),
            ]
        )
        game.players[1].hand.tiles = [Tile.C8, Tile.C8, Tile.C8, Tile.C8]
        game.players[2].hand.tiles = [Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C7]

        next_step0 = game.check_draw_next_step()
        self.assertEqual(0, next_step0[0]["kong"]["player"])
        self.assertEqual("add_kong", next_step0[0]["kong"]["type"])
        game.turn_next()

        next_step1 = game.check_draw_next_step()
        self.assertEqual(1, next_step1[0]["kong"]["player"])
        self.assertEqual("closed_kong", next_step1[0]["kong"]["type"])
        game.turn_next()

        next_step2 = game.check_draw_next_step()
        self.assertEqual(2, next_step2[0]["win"]["player"])

    def test_step(self):
        # error test
        error_test_game = Game()
        self.assertRaises(AttributeError, error_test_game.step, Action.DISCARD, 0)
        self.assertRaises(
            AttributeError,
            error_test_game.step,
            Action.CHOW,
            0,
            tiles=TripletMeld((Tile.D3, Tile.D3, Tile.D3)),
        )
        self.assertRaises(
            AttributeError,
            error_test_game.step,
            Action.PONG,
            0,
            tiles=SequenceMeld((Tile.D6, Tile.D7, Tile.D8)),
        )
        self.assertRaises(
            AttributeError,
            error_test_game.step,
            Action.KONG,
            0,
            tiles=SequenceMeld((Tile.D6, Tile.D7, Tile.D8)),
        )
        self.assertRaises(
            AttributeError,
            error_test_game.step,
            Action.CLOSEDKONG,
            0,
            tiles=TripletMeld((Tile.D3, Tile.D3, Tile.D3)),
        )
        self.assertRaises(AttributeError, error_test_game.step, Action.ADDKONG, 0)
        # -------------------------------------
        game = Game()
        game.players[0].hand.tiles = [Tile.C2, Tile.C2, Tile.C2, Tile.D7, Tile.W1]
        game.players[3].hand.tiles = [Tile.D3, Tile.D3, Tile.C7, Tile.C7, Tile.C2]
        game.players[2].hand.tiles = [Tile.C7, Tile.C7, Tile.C7, Tile.W2]
        game.players[1].hand.tiles = [
            Tile.D6,
            Tile.D8,
            Tile.D3,
            Tile.B1,
            Tile.B1,
            Tile.B1,
        ]

        game.step(Action.DISCARD, 0, tile=Tile.D7)
        game.step(Action.CHOW, 1, tiles=SequenceMeld((Tile.D6, Tile.D7, Tile.D8)))
        game.step(Action.DISCARD, 1, tile=Tile.D3)
        game.step(Action.PONG, 3, tiles=TripletMeld((Tile.D3, Tile.D3, Tile.D3)))
        game.step(Action.DISCARD, 3, tile=Tile.C2)
        game.step(
            Action.KONG, 0, tiles=QuadrupletMeld((Tile.C2, Tile.C2, Tile.C2, Tile.C2))
        )
        game.step(Action.DISCARD, 0, tile=Tile.W1)
        game.step(Action.NOTHING, 0)
        game.players[1].draw(Tile.B1)
        game.step(
            Action.CLOSEDKONG,
            1,
            tiles=QuadrupletMeld((Tile.B1, Tile.B1, Tile.B1, Tile.B1)),
        )
        game.players[3].draw(Tile.D3)
        game.step(Action.ADDKONG, 3, tile=Tile.D3)
        game.players[0].draw(Tile.W2)
        game.step(Action.DISCARD, 0, tile=Tile.W2)
        game.step(Action.WIN, 2)
        # -------------------------------------
        game = Game()
        game.board.wall = []
        game.step(Action.NOTHING, 0)

    def test_get_observation(self):
        game = Game()
        game.players[0].hand = [Tile.C2, Tile.C2, Tile.C2]
        game.players[1].declaration = Declaration(
            [
                TripletMeld((Tile.D3, Tile.D3, Tile.D3)),
            ]
        )
        game.players[2].declaration = Declaration(
            [
                SequenceMeld((Tile.D1, Tile.D2, Tile.D3)),
            ]
        )
        game.players[3].declaration = Declaration(
            [
                QuadrupletMeld((Tile.D5, Tile.D5, Tile.D5, Tile.D5)),
            ]
        )
        observation = game.get_observation()

        self.assertEqual(3, observation[int(Tile.C2)])
        self.assertEqual(1, observation[34 + int(Tile.D1)])
        self.assertEqual(1, observation[34 + int(Tile.D2)])
        self.assertEqual(4, observation[34 + int(Tile.D3)])
        self.assertEqual(4, observation[34 + int(Tile.D5)])
